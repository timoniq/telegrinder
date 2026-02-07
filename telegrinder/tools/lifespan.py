import asyncio
import dataclasses
import datetime
import typing
from contextlib import asynccontextmanager
from inspect import iscoroutine, iscoroutinefunction

from kungfu import Error, Ok, Result
from nodnod.error import NodeError

from telegrinder.modules import logger
from telegrinder.tools.aio import next_generator, run_task, stop_generator
from telegrinder.tools.fullname import fullname

if typing.TYPE_CHECKING:
    from telegrinder.tools.magic.function import Function

type CoroutineTask[T] = typing.Coroutine[typing.Any, typing.Any, T]
type CoroutineFunc[**P, T] = typing.Callable[P, CoroutineTask[T]]
type Task[**P, T] = CoroutineFunc[P, T] | CoroutineTask[T] | DelayedTask[P]


def to_coroutine_task[T](task: Task[..., T], /) -> CoroutineTask[T]:
    if iscoroutinefunction(task) or isinstance(task, DelayedTask):
        task = task()
    elif not iscoroutine(task):
        raise TypeError("Task should be coroutine, coroutine function or delayed task.")
    return task


@dataclasses.dataclass
class DelayedTask[**P]:
    _cancelled: bool = dataclasses.field(default=False, init=False, repr=False)
    _event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event, init=False, repr=False)
    _timer: asyncio.TimerHandle | None = dataclasses.field(default=None, init=False, repr=False)

    function: Function[P, typing.Any]
    seconds: float | datetime.timedelta
    repeat: bool = dataclasses.field(default=False, kw_only=True)

    def __post_init__(self) -> None:
        self.function.cancel = self.cancel

    async def __call__(self) -> typing.Any:
        from telegrinder.node.compose import compose_once

        stopped = False

        while not stopped and not self.is_cancelled:
            self.start_timer()
            await self._event.wait()

            try:
                async with compose_once(self.function) as result:
                    result.unwrap()
            except Exception:
                await logger.aexception(
                    "Delayed task `{}` failed with exception, traceback message below:",
                    fullname(self.function),
                )
            finally:
                self._event.clear()
                self._timer = None

                if not self.repeat:
                    stopped = True

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    @property
    def delay(self) -> float:
        return float(self.seconds) if isinstance(self.seconds, int | float) else self.seconds.total_seconds()

    def start_timer(self) -> None:
        if self._timer is None:
            self._timer = asyncio.get_running_loop().call_later(
                self.delay,
                callback=lambda: self._event.set() if not self._event.is_set() else None,
            )

    def cancel(self) -> bool:
        if self._cancelled:
            return True

        self._cancelled = True

        if self._timer is None or self._timer.cancelled():
            self._timer = None
            return False

        self._timer.cancel()
        self._timer = None

        for future in self._event._waiters:
            if not future.cancelled():
                future.cancel()

        return True


@dataclasses.dataclass(kw_only=True, slots=True, repr=False)
class Lifespan:
    _started: bool = dataclasses.field(default=False, init=False)
    _lifespan_generator: typing.AsyncGenerator[Result[typing.Any, NodeError], None] | None = dataclasses.field(
        default=None,
        init=False,
    )
    lifespan_function: typing.Callable[[], typing.AsyncContextManager[typing.Any]] | None = dataclasses.field(
        default=None
    )
    startup_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    startup_coro_task_functions: list[CoroutineFunc[..., typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_coro_task_functions: list[CoroutineFunc[..., typing.Any]] = dataclasses.field(default_factory=lambda: [])

    def __repr__(self) -> str:
        return "<{}: started={}>".format(fullname(self), self._started)

    def __add__(self, other: object, /) -> typing.Self:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.__class__(
            startup_tasks=self.startup_tasks + other.startup_tasks,
            shutdown_tasks=self.shutdown_tasks + other.shutdown_tasks,
        )

    def __iadd__(self, other: object, /) -> typing.Self:
        if not isinstance(other, self.__class__):
            return NotImplemented

        self.startup_tasks.extend(other.startup_tasks)
        self.shutdown_tasks.extend(other.shutdown_tasks)
        return self

    async def __aenter__(self) -> None:
        await self._start()

    async def __aexit__(
        self,
        exc_type: typing.Any | None,
        exc_value: typing.Any | None,
        exc_tb: typing.Any | None,
    ) -> None:
        await self._shutdown()

    def __call__[Function: typing.Callable[..., typing.AsyncGenerator[typing.Any]]](
        self,
        func: Function,
        /,
    ) -> Function:
        self.lifespan_function = asynccontextmanager(func)
        return func

    @property
    def started(self) -> bool:
        return self._started

    @staticmethod
    async def _run_tasks(tasks: list[CoroutineTask[typing.Any]], /) -> None:
        while tasks:
            await tasks.pop(0)

    @staticmethod
    async def _run_coro_task_functions(tasks: list[CoroutineFunc[..., typing.Any]], /) -> None:
        from telegrinder.node.compose import compose_once

        while tasks:
            async with compose_once(tasks.pop(0)) as result:
                match result:
                    case Error(error):
                        await logger.aerror(
                            "Coroutine task function `{}` failed with error: {}\n",
                            fullname(tasks.pop(0)),
                            NodeError(
                                f"* failed to compose coroutine task function `{fullname(tasks.pop(0))}`",
                                from_error=error,
                            ),
                        )

    async def _start(self) -> None:
        from telegrinder.node.compose import compose_once

        if not self._started:
            await logger.adebug("Running lifespan startup tasks")
            self._started = True

            if self.lifespan_function is not None:
                self._lifespan_generator = getattr(compose_once(self.lifespan_function), "gen", None)

                if self._lifespan_generator is not None:
                    match await next_generator(self._lifespan_generator):
                        case Ok(gen):
                            await next_generator(gen.gen)
                            await stop_generator(self._lifespan_generator)
                            self._lifespan_generator = gen.gen
                        case Error(error):
                            await logger.aerror(
                                "Lifespan function `{}` failed with error: {}\n",
                                fullname(self.lifespan_function),
                                NodeError(
                                    f"* failed to compose lifespan function `{fullname(self.lifespan_function)}`",
                                    from_error=error,
                                ),
                            )
                            await stop_generator(self._lifespan_generator)

            await self._run_coro_task_functions(self.startup_coro_task_functions)
            await self._run_tasks(self.startup_tasks)

    async def _shutdown(self) -> None:
        if self._started:
            await logger.adebug("Running lifespan shutdown tasks")
            self._started = False

            if self._lifespan_generator is not None:
                await stop_generator(self._lifespan_generator)
                self._lifespan_generator = None

            await self._run_coro_task_functions(self.shutdown_coro_task_functions)
            await self._run_tasks(self.shutdown_tasks)

    def start(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        run_task(self._start(), loop=loop)

    def shutdown(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        run_task(self._shutdown(), loop=loop)

    def add_startup_task[**P, T](self, task: Task[P, T], /) -> None:
        self.startup_tasks.append(to_coroutine_task(task))

    def add_shutdown_task[**P, T](self, task: Task[P, T], /) -> None:
        self.shutdown_tasks.append(to_coroutine_task(task))

    def on_startup[**P, T](self, task: CoroutineFunc[P, T], /) -> CoroutineFunc[P, T]:
        self.startup_coro_task_functions.append(task)
        return task

    def on_shutdown[**P, T](self, task: CoroutineFunc[P, T], /) -> CoroutineFunc[P, T]:
        self.shutdown_coro_task_functions.append(task)
        return task


__all__ = ("CoroutineTask", "DelayedTask", "Lifespan", "run_task", "to_coroutine_task")
