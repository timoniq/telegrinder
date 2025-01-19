import asyncio
import contextlib
import datetime
import typing

from telegrinder.modules import logger
from telegrinder.tools.lifespan import (
    CoroutineFunc,
    CoroutineTask,
    DelayedTask,
    Lifespan,
    Task,
    to_coroutine_task,
)
from telegrinder.tools.loop_wrapper.abc import ABCLoopWrapper
from telegrinder.tools.magic import cancel_future


class LoopWrapper(ABCLoopWrapper):
    def __init__(
        self,
        *,
        tasks: list[CoroutineTask[typing.Any]] | None = None,
        lifespan: Lifespan | None = None,
    ) -> None:
        self.tasks: list[CoroutineTask[typing.Any]] = tasks or []
        self.lifespan = lifespan or Lifespan()
        self._loop: asyncio.AbstractEventLoop | None = None

    @property
    def is_running(self) -> bool:
        if self._loop is None:
            return False
        return self._loop.is_running()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        assert self._loop is not None, "Loop is not set."
        return self._loop

    def __repr__(self) -> str:
        return "<{}: loop={!r} with tasks={!r}, lifespan={!r}>".format(
            self.__class__.__name__,
            self._loop,
            self.tasks,
            self.lifespan,
        )

    def run_event_loop(self) -> typing.NoReturn:  # type: ignore
        if not self.tasks:
            logger.warning("Run loop without tasks!")

        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop()

        self.lifespan.start()
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
                    except BaseException:
                        logger.exception("Traceback message below:")
                tasks = asyncio.all_tasks(self._loop)
        except KeyboardInterrupt:
            print()  # blank print for ^C
            logger.info("Caught KeyboardInterrupt, cancellation...")
            self.complete_tasks(tasks)
        finally:
            self.lifespan.shutdown()
            if self._loop.is_running():
                self._loop.close()

    def add_task(self, task: Task[..., typing.Any], /) -> None:
        task = to_coroutine_task(task)

        if self._loop is not None and self._loop.is_running():
            self._loop.create_task(task)
        else:
            self.tasks.append(task)

    def complete_tasks(self, tasks: set[asyncio.Task[typing.Any]], /) -> None:
        tasks = tasks | asyncio.all_tasks(self.loop)
        with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
            self.loop.run_until_complete(cancel_future(asyncio.gather(*tasks, return_exceptions=True)))

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

        def decorator[Func: CoroutineFunc[..., typing.Any]](func: Func) -> Func:
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

        def decorator[Func: CoroutineFunc[..., typing.Any]](func: Func) -> Func:
            self.add_task(DelayedTask(func, seconds, repeat=True))
            return func

        return decorator


__all__ = ("DelayedTask", "LoopWrapper", "to_coroutine_task")
