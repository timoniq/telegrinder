import asyncio
import contextlib
import dataclasses
import datetime
import typing

from telegrinder.modules import logger
from telegrinder.tools.loop_wrapper.abc import ABCLoopWrapper

T = typing.TypeVar("T")
P = typing.ParamSpec("P")
CoroFunc = typing.TypeVar("CoroFunc", bound="CoroutineFunc[..., typing.Any]")

CoroutineTask: typing.TypeAlias = typing.Coroutine[typing.Any, typing.Any, T]
CoroutineFunc: typing.TypeAlias = typing.Callable[P, CoroutineTask[T]]
Task: typing.TypeAlias = (
    "CoroutineFunc[P, T] | CoroutineTask[T] | DelayedTask[typing.Callable[P, CoroutineTask[T]]]"
)


def run_tasks(
    tasks: list[CoroutineTask[typing.Any]],
    loop: asyncio.AbstractEventLoop,
) -> None:
    while tasks:
        loop.run_until_complete(tasks.pop(0))


def to_coroutine_task(task: Task) -> CoroutineTask[typing.Any]:
    if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
        task = task()
    elif not asyncio.iscoroutine(task):
        raise TypeError("Task should be coroutine or coroutine function.")
    return task


@dataclasses.dataclass(slots=True)
class DelayedTask(typing.Generic[CoroFunc]):
    handler: CoroFunc
    seconds: float
    repeat: bool = dataclasses.field(default=False, kw_only=True)
    _cancelled: bool = dataclasses.field(default=False, init=False, repr=False)

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        while not self.is_cancelled:
            await asyncio.sleep(self.seconds)
            if self.is_cancelled:
                break
            try:
                await self.handler(*args, **kwargs)
            finally:
                if not self.repeat:
                    break

    def cancel(self) -> None:
        if not self._cancelled:
            self._cancelled = True


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class Lifespan:
    startup_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])

    def on_startup(self, task: Task, /) -> Task:
        self.startup_tasks.append(to_coroutine_task(task))
        return task

    def on_shutdown(self, task: Task, /) -> Task:
        self.shutdown_tasks.append(to_coroutine_task(task))
        return task

    def start(self, loop: asyncio.AbstractEventLoop, /) -> None:
        run_tasks(self.startup_tasks, loop)

    def shutdown(self, loop: asyncio.AbstractEventLoop, /) -> None:
        run_tasks(self.shutdown_tasks, loop)


class LoopWrapper(ABCLoopWrapper):
    def __init__(
        self,
        *,
        tasks: list[CoroutineTask[typing.Any]] | None = None,
        lifespan: Lifespan | None = None,
        event_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self.tasks: list[CoroutineTask[typing.Any]] = tasks or []
        self.lifespan = lifespan or Lifespan()
        self._loop = event_loop

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        assert self._loop is not None
        return self._loop

    def __repr__(self) -> str:
        return "<{}: loop={!r} with tasks={!r}, lifespan={!r}>".format(
            self.__class__.__name__,
            self._loop,
            self.tasks,
            self.lifespan,
        )

    def run_event_loop(self) -> None:
        if not self.tasks:
            logger.warning("You run loop with 0 tasks!")

        self._loop = asyncio.new_event_loop() if self._loop is None else self._loop
        self.lifespan.start(self._loop)

        while self.tasks:
            self._loop.create_task(self.tasks.pop(0))

        tasks = asyncio.all_tasks(self._loop)
        try:
            while tasks:
                tasks_results, _ = self._loop.run_until_complete(
                    asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION),
                )
                for task_result in tasks_results:
                    try:
                        task_result.result()
                    except BaseException as ex:
                        logger.exception(ex)
                tasks = asyncio.all_tasks(self._loop)
        except KeyboardInterrupt:
            print()  # blank print for ^C
            logger.info("Caught KeyboardInterrupt, cancellation...")
            self.complete_tasks(tasks)
        finally:
            self.lifespan.shutdown(self._loop)
            if self._loop.is_running():
                self._loop.close()

    def add_task(self, task: Task) -> None:
        task = to_coroutine_task(task)

        if self._loop is not None and self._loop.is_running():
            self._loop.create_task(task)
        else:
            self.tasks.append(task)

    def complete_tasks(self, tasks: set[asyncio.Task[typing.Any]]) -> None:
        tasks = tasks | asyncio.all_tasks(self.loop)
        task_to_cancel = asyncio.gather(*tasks, return_exceptions=True)
        task_to_cancel.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            self.loop.run_until_complete(task_to_cancel)

    @typing.overload
    def timer(self, *, seconds: datetime.timedelta) -> typing.Callable[..., typing.Any]: ...

    @typing.overload
    def timer(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0,
    ) -> typing.Callable[..., typing.Any]: ...

    def timer(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float | datetime.timedelta = 0,
    ) -> typing.Callable[..., typing.Any]:
        if isinstance(seconds, datetime.timedelta):
            seconds = seconds.total_seconds()

        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: CoroFunc) -> CoroFunc:
            self.add_task(DelayedTask(func, seconds, repeat=False))
            return func

        return decorator

    @typing.overload
    def interval(self, *, seconds: datetime.timedelta) -> typing.Callable[..., typing.Any]: ...

    @typing.overload
    def interval(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0,
    ) -> typing.Callable[..., typing.Any]: ...

    def interval(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float | datetime.timedelta = 0,
    ) -> typing.Callable[..., typing.Any]:
        if isinstance(seconds, datetime.timedelta):
            seconds = seconds.total_seconds()

        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: CoroFunc) -> CoroFunc:
            self.add_task(DelayedTask(func, seconds, repeat=True))
            return func

        return decorator


__all__ = ("DelayedTask", "Lifespan", "LoopWrapper", "to_coroutine_task")
