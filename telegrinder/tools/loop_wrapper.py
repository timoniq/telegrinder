import asyncio
import contextlib
import datetime
import enum
import typing

from telegrinder.modules import logger
from telegrinder.tools.aio import cancel_future, run_task
from telegrinder.tools.final import Final
from telegrinder.tools.fullname import fullname
from telegrinder.tools.lifespan import (
    CoroutineFunc,
    CoroutineTask,
    DelayedTask,
    Lifespan,
    Task,
    to_coroutine_task,
)
from telegrinder.tools.singleton.singleton import Singleton

type Tasks = set[asyncio.Task[typing.Any]]
type LoopFactory = typing.Callable[[], asyncio.AbstractEventLoop]
type DelayedFunctionDecorator[**P, R] = typing.Callable[[typing.Callable[P, R]], DelayedFunction[P, R]]


class DelayedFunction[**P, R](typing.Protocol):
    __name__: str
    __delayed_task__: DelayedTask

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> typing.Coroutine[typing.Any, typing.Any, R]: ...

    def cancel(self) -> bool:
        """Cancel delayed task."""
        ...


@enum.unique
class LoopWrapperState(enum.Enum):
    NOT_RUNNING = enum.auto()
    RUNNING = enum.auto()
    RUNNING_MANUALLY = enum.auto()
    SHUTDOWN = enum.auto()


@typing.final
class LoopWrapper(Singleton, Final):
    _loop: asyncio.AbstractEventLoop
    _lifespan: Lifespan
    _tasks: list[CoroutineTask[typing.Any]]
    _state: LoopWrapperState
    _all_tasks: set[asyncio.Task[typing.Any]]

    __slots__ = ("_loop", "_lifespan", "_tasks", "_state", "_all_tasks")

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._lifespan = Lifespan()
        self._tasks = list()
        self._state = LoopWrapperState.NOT_RUNNING
        self._all_tasks = set()

        self._loop.create_task(self._run_async_event_loop())

    def __call__(self) -> asyncio.AbstractEventLoop:
        """A loop factory."""
        return self._loop

    def __repr__(self) -> str:
        return "<{}: loop={!r} lifespan={!r}>".format(
            fullname(self) + (" (running)" if self.running else ""),
            self._loop,
            self._lifespan,
        )

    async def _run_async_event_loop(self) -> None:
        if not self.running:
            self._state = LoopWrapperState.RUNNING
            async with self._async_wrap_loop():
                await self._run()

    async def _run(self) -> None:
        logger.debug("Running loop wrapper")

        while self._tasks:
            self._loop.create_task(self._tasks.pop(0))

        while self.running and (tasks := self._get_all_tasks()):
            await self._process_tasks(tasks)

    async def _process_tasks(self, tasks: Tasks, /) -> None:
        """Processes the given tasks, checks for exceptions, and raises them if any."""

        tasks_results, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
        for task_result in tasks_results:
            try:
                if not task_result.cancelled() and (exception := task_result.exception()) is not None:
                    raise exception from None  # Raise the exception that was set on the task.
            except BaseException:
                logger.exception("Traceback message below:")

    async def _cancel_tasks(self) -> None:
        with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
            await cancel_future(asyncio.gather(*self._get_all_tasks(), return_exceptions=True))

    @contextlib.asynccontextmanager
    async def _async_wrap_loop(self) -> typing.AsyncGenerator[typing.Any, None]:
        try:
            await self._lifespan._start()
            yield
        except asyncio.CancelledError:
            logger.info("LoopWrapper task was cancelled, cancellation tasks...")
            await self._cancel_tasks()
        finally:
            await self._shutdown()

    async def _shutdown(self) -> None:
        await self.lifespan._shutdown()
        logger.debug("Shutdown loop wrapper")
        self._state = LoopWrapperState.SHUTDOWN

    def _get_all_tasks(self) -> Tasks:
        """Get a set of all tasks from the loop (`exclude the current task if any`)."""

        return (self._all_tasks | asyncio.all_tasks(loop=self._loop)).symmetric_difference(
            set() if (task := asyncio.current_task(self.loop)) is None else {task},
        )

    def _close_loop(self) -> None:
        if not self._loop.is_closed():
            logger.debug("Closing event loop {!r}", self._loop)
            self._loop.close()

    @contextlib.contextmanager
    def _wrap_loop(self, *, close_loop: bool = True) -> typing.Generator[typing.Any, None, None]:
        try:
            self.lifespan.start()
            yield
        except KeyboardInterrupt:
            logger.info("Caught KeyboardInterrupt, cancellation tasks...")
            run_task(self._cancel_tasks())
        finally:
            run_task(self._shutdown())
            if close_loop:
                self._close_loop()

    def _get_delayed_task_decorator(
        self,
        repeat: bool,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float | datetime.timedelta = 0.0,
    ) -> typing.Callable[..., typing.Any]:
        if isinstance(seconds, int | float):
            seconds += minutes * 60
            seconds += hours * 60 * 60
            seconds += days * 24 * 60 * 60

        def decorator[Func: CoroutineFunc[..., typing.Any]](function: Func) -> Func:
            self.add_task(DelayedTask(function, seconds, repeat=repeat))
            return function

        return decorator

    @property
    def lifespan(self) -> Lifespan:
        return self._lifespan

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def running(self) -> bool:
        return self._state in {LoopWrapperState.RUNNING, LoopWrapperState.RUNNING_MANUALLY}

    @property
    def shutdown(self) -> bool:
        return self._state is LoopWrapperState.SHUTDOWN

    def run(self, *, close_loop: bool = True) -> typing.NoReturn:  # type: ignore
        if self.running:
            raise RuntimeError("Loop wrapper already running.")

        self._state = LoopWrapperState.RUNNING_MANUALLY
        with self._wrap_loop(close_loop=close_loop):
            run_task(self._run())

    @typing.overload
    def bind_loop(self, *, loop_factory: LoopFactory) -> typing.Self: ...

    @typing.overload
    def bind_loop(self, *, loop: asyncio.AbstractEventLoop) -> typing.Self: ...

    def bind_loop(
        self,
        *,
        loop_factory: LoopFactory | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> typing.Self:
        assert loop is not None or loop_factory is not None

        if self.running:
            logger.warning("Cannot bind a new event loop to running loop wrapper.")
            return self

        old_loop = self._loop
        self._loop = loop_factory() if loop_factory else loop or self._loop

        if old_loop is not self._loop:
            self._loop.create_task(self._run_async_event_loop())

        return self

    def add_task(self, task: Task[..., typing.Any], /) -> None:
        coro = to_coroutine_task(task)

        if self.running:
            new_task = self._loop.create_task(coro)
            self._all_tasks.add(new_task)
            new_task.add_done_callback(self._all_tasks.discard)
        else:
            self._tasks.append(coro)

    @typing.overload
    def timer[**P, R](self, delta: datetime.timedelta, /) -> DelayedFunctionDecorator[P, R]: ...

    @typing.overload
    def timer[**P, R](
        self,
        *,
        days: int = ...,
        hours: int = ...,
        minutes: int = ...,
        seconds: float = ...,
    ) -> DelayedFunctionDecorator[P, R]: ...

    def timer(
        self,
        delta: datetime.timedelta | None = None,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0.0,
    ) -> DelayedFunctionDecorator[..., typing.Any]:
        return self._get_delayed_task_decorator(
            repeat=False,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=delta or seconds,
        )

    @typing.overload
    def interval[**P, R](self, delta: datetime.timedelta, /) -> DelayedFunctionDecorator[P, R]: ...

    @typing.overload
    def interval[**P, R](
        self,
        *,
        days: int = ...,
        hours: int = ...,
        minutes: int = ...,
        seconds: float = ...,
    ) -> DelayedFunctionDecorator[P, R]: ...

    def interval(
        self,
        delta: datetime.timedelta | None = None,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0.0,
    ) -> DelayedFunctionDecorator[..., typing.Any]:
        return self._get_delayed_task_decorator(
            repeat=True,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=delta or seconds,
        )


__all__ = ("DelayedTask", "LoopWrapper", "to_coroutine_task")
