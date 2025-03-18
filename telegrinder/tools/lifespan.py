import asyncio
import dataclasses
import datetime
import typing

from telegrinder.modules import logger

type CoroutineTask[T] = typing.Coroutine[typing.Any, typing.Any, T]
type CoroutineFunc[**P, T] = typing.Callable[P, CoroutineTask[T]]
type Task[**P, T] = CoroutineFunc[P, T] | CoroutineTask[T] | DelayedTask[typing.Callable[P, CoroutineTask[T]]]


def run_tasks(*tasks: CoroutineTask[typing.Any]) -> None:
    loop = asyncio.get_event_loop()
    for task in tasks:
        loop.run_until_complete(future=task)


def to_coroutine_task[**P, T](task: Task[P, T], /) -> CoroutineTask[T]:
    if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
        task = task()
    elif not asyncio.iscoroutine(task):
        raise TypeError("Task should be coroutine or coroutine function.")
    return task


@dataclasses.dataclass
class DelayedTask[Function: CoroutineFunc[..., typing.Any]]:
    function: Function
    seconds: float | datetime.timedelta
    repeat: bool = dataclasses.field(default=False, kw_only=True)
    _cancelled: bool = dataclasses.field(default=False, init=False, repr=False)
    _task: asyncio.Task[typing.Any] | None = dataclasses.field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self.function.cancel = self.cancel

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    @property
    def delay(self) -> float:
        return self.seconds if isinstance(self.seconds, int | float) else self.seconds.total_seconds()

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        self._task = self._task or asyncio.current_task()
        stopped = False

        while not self.is_cancelled and not stopped:
            await asyncio.sleep(self.delay)
            if self.is_cancelled:
                break
            try:
                await self.function(*args, **kwargs)
            except BaseException:
                logger.exception(
                    "Delayed task for function {!r} caught an exception, traceback message below:",
                    self.function.__name__,
                )
            finally:
                stopped = not self.repeat

    def cancel(self) -> bool:
        if not self._cancelled:
            self._cancelled = True
            if self._task is not None:
                self._task.cancel()
                self._task = None

            return True

        return False


@dataclasses.dataclass(kw_only=True, slots=True)
class Lifespan:
    startup_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    _is_started: bool = dataclasses.field(default=False, init=False)

    def __enter__(self) -> None:
        self.start()

    def __exit__(self, *args: typing.Any) -> None:
        self.shutdown()

    async def __aenter__(self) -> None:
        if self.startup_tasks and not self._is_started:
            self._start()
            await self._arun_tasks(self.startup_tasks)

    async def __aexit__(self, *args: typing.Any) -> None:
        if self.shutdown_tasks and self._is_started:
            self._shutdown()
            await self._arun_tasks(self.shutdown_tasks)

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

    def on_startup[**P, T](self, task: Task[P, T], /) -> Task[P, T]:
        self.startup_tasks.append(to_coroutine_task(task))
        return task

    def on_shutdown[**P, T](self, task: Task[P, T], /) -> Task[P, T]:
        self.shutdown_tasks.append(to_coroutine_task(task))
        return task

    @staticmethod
    def _run_tasks(tasks: list[CoroutineTask[typing.Any]], /) -> None:
        run_tasks(*tasks)
        tasks.clear()

    @staticmethod
    async def _arun_tasks(tasks: list[CoroutineTask[typing.Any]], /) -> None:
        while tasks:
            await tasks.pop(0)

    def _start(self) -> None:
        logger.debug("Running lifespan startup tasks")
        self._is_started = True
    
    def _shutdown(self) -> None:
        logger.debug("Running lifespan shutdown tasks")
        self._is_started = False

    def start(self) -> None:
        if self.startup_tasks and not self._is_started:
            self._start()
            self._run_tasks(self.startup_tasks)

    def shutdown(self) -> None:
        if self.shutdown_tasks and self._is_started:
            self._shutdown()
            self._run_tasks(self.shutdown_tasks)


__all__ = (
    "CoroutineTask",
    "DelayedTask",
    "Lifespan",
    "run_tasks",
    "to_coroutine_task",
)
