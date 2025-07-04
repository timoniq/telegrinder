import asyncio
import dataclasses
import datetime
import typing

from telegrinder.modules import logger
from telegrinder.tools.aio import run_task
from telegrinder.tools.fullname import fullname

type CoroutineTask[T] = typing.Coroutine[typing.Any, typing.Any, T]
type CoroutineFunc[**P, T] = typing.Callable[P, CoroutineTask[T]]
type Task[**P, T] = CoroutineFunc[P, T] | CoroutineTask[T] | DelayedTask[typing.Callable[P, CoroutineTask[T]]]


def to_coroutine_task[**P, T](task: Task[P, T], /) -> CoroutineTask[T]:
    if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
        task = task()
    elif not asyncio.iscoroutine(task):
        raise TypeError("Task should be coroutine or coroutine function.")
    return task


@dataclasses.dataclass
class DelayedTask[Function: CoroutineFunc[..., typing.Any]]:
    _cancelled: bool = dataclasses.field(default=False, init=False, repr=False)
    _task: asyncio.Task[typing.Any] | None = dataclasses.field(default=None, init=False, repr=False)

    function: Function
    seconds: float | datetime.timedelta
    repeat: bool = dataclasses.field(default=False, kw_only=True)

    def __post_init__(self) -> None:
        self.function.cancel = self.cancel

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    @property
    def delay(self) -> float:
        return float(self.seconds) if isinstance(self.seconds, int | float) else self.seconds.total_seconds()

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        self._task = self._task or asyncio.current_task()
        stopped = False

        while not self._cancelled and not stopped:
            await asyncio.sleep(self.delay)
            try:
                await self.function(*args, **kwargs)
            except BaseException:
                logger.exception(
                    "Delayed task for function `{}` caught an exception, traceback message below:",
                    fullname(self.function),
                )
            finally:
                stopped = not self.repeat

    def cancel(self) -> bool:
        if not self._cancelled:
            self._cancelled = True if self._task is None else self._task.cancel()
            self._task = None

        return self._cancelled


@dataclasses.dataclass(kw_only=True, slots=True, repr=False)
class Lifespan:
    _started: bool = dataclasses.field(default=False, init=False)
    startup_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])

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

    def __enter__(self) -> None:
        self.start()

    def __exit__(self, *args: typing.Any) -> None:
        self.shutdown()

    async def __aenter__(self) -> None:
        await self._start()

    async def __aexit__(self, *args: typing.Any) -> None:
        await self._shutdown()

    @property
    def started(self) -> bool:
        return self._started

    @staticmethod
    async def _run_tasks(tasks: list[CoroutineTask[typing.Any]], /) -> None:
        while tasks:
            await tasks.pop(0)

    async def _start(self) -> None:
        if not self._started:
            logger.debug("Running lifespan startup tasks")
            self._started = True
            await self._run_tasks(self.startup_tasks)

    async def _shutdown(self) -> None:
        if self._started:
            logger.debug("Running lifespan shutdown tasks")
            self._started = False
            await self._run_tasks(self.shutdown_tasks)

    def start(self) -> None:
        run_task(self._start())

    def shutdown(self) -> None:
        run_task(self._shutdown())

    def on_startup[**P, T](self, task: Task[P, T], /) -> Task[P, T]:
        self.startup_tasks.append(to_coroutine_task(task))
        return task

    def on_shutdown[**P, T](self, task: Task[P, T], /) -> Task[P, T]:
        self.shutdown_tasks.append(to_coroutine_task(task))
        return task


__all__ = ("CoroutineTask", "DelayedTask", "Lifespan", "run_task", "to_coroutine_task")
