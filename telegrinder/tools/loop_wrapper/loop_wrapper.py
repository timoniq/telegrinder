import asyncio
import contextlib
import dataclasses
import traceback
import typing

from telegrinder.modules import logger

from .abc import ABCLoopWrapper

T = typing.TypeVar("T")
P = typing.ParamSpec("P")
CoroFunc = typing.TypeVar("CoroFunc", bound="CoroutineFunc")

CoroutineTask: typing.TypeAlias = typing.Coroutine[typing.Any, typing.Any, T]
CoroutineFunc: typing.TypeAlias = typing.Callable[P, CoroutineTask[T]]
Task: typing.TypeAlias = typing.Union[CoroutineFunc, CoroutineTask, "DelayedTask"]


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


@dataclasses.dataclass
class DelayedTask(typing.Generic[CoroFunc]):
    handler: CoroFunc
    seconds: float
    repeat: bool = dataclasses.field(default=False, kw_only=True)
    _cancelled: bool = dataclasses.field(default=False, init=False, repr=False)

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    async def __call__(self, *args, **kwargs) -> None:
        while not self.is_cancelled:
            await asyncio.sleep(self.seconds)
            if self.is_cancelled:
                break
            try:
                await self.handler(*args, **kwargs)
            except Exception as e:
                logger.error("Error in task %s", str(e))
                traceback.print_exc()
            if not self.repeat:
                break

    def cancel(self) -> None:
        if not self._cancelled:
            self._cancelled = True


@dataclasses.dataclass(kw_only=True)
class Lifespan:
    startup_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])
    shutdown_tasks: list[CoroutineTask[typing.Any]] = dataclasses.field(default_factory=lambda: [])

    def on_startup(self, task_or_func: Task) -> Task:
        self.startup_tasks.append(to_coroutine_task(task_or_func))
        return task_or_func

    def on_shutdown(self, task_or_func: Task) -> Task:
        self.shutdown_tasks.append(to_coroutine_task(task_or_func))
        return task_or_func

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        run_tasks(self.startup_tasks, loop)

    def shutdown(self, loop: asyncio.AbstractEventLoop) -> None:
        run_tasks(self.shutdown_tasks, loop)


class LoopWrapper(ABCLoopWrapper):
    def __init__(
        self,
        *,
        tasks: list[CoroutineTask[typing.Any]] | None = None,
        lifespan: Lifespan | None = None,
    ) -> None:
        self.tasks: list[CoroutineTask[typing.Any]] = tasks or []
        self.lifespan = lifespan or Lifespan()
        self._loop = asyncio.new_event_loop()

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

        if self._loop and self._loop.is_running():
            self._loop.create_task(task)
        else:
            self.tasks.append(task)

    def complete_tasks(self, tasks: set[asyncio.Task[typing.Any]]) -> None:
        tasks = tasks | asyncio.all_tasks(self._loop)
        task_to_cancel = asyncio.gather(*tasks, return_exceptions=True)
        task_to_cancel.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            self._loop.run_until_complete(task_to_cancel)

    def timer(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0,
    ):
        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: CoroFunc) -> CoroFunc:
            self.add_task(DelayedTask(func, seconds, repeat=False))
            return func

        return decorator

    def interval(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0,
    ):
        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: CoroFunc) -> CoroFunc:
            self.add_task(DelayedTask(func, seconds, repeat=True))
            return func

        return decorator


__all__ = ("DelayedTask", "Lifespan", "LoopWrapper", "to_coroutine_task")
