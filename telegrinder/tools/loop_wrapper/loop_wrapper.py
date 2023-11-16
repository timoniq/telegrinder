import asyncio
import contextlib
import dataclasses
import typing

from telegrinder.modules import logger

from .abc import ABCLoopWrapper, CoroutineFunc, CoroutineTask

ExceptionT = typing.TypeVar("ExceptionT", bound=BaseException)
ErrorHandler = typing.Callable[[ExceptionT], CoroutineTask]


async def keyboard_interrupt_handler(_: KeyboardInterrupt):
    print()  #: for ^C
    logger.info("KeyboardInterrupt")


async def system_exit_handler(exc: SystemExit):
    logger.info(f"System exit with code {exc.code}")


DEFAULT_ERROR_HANDLERS: dict[type[BaseException], list[ErrorHandler]] = {
    KeyboardInterrupt: [keyboard_interrupt_handler],
    SystemExit: [system_exit_handler],
}


@dataclasses.dataclass(frozen=True)
class DelayedTask:
    handler: CoroutineFunc
    seconds: float
    repeat: bool = dataclasses.field(default=False, kw_only=True)

    async def __call__(self, *args, **kwargs) -> None:
        while True:
            await asyncio.sleep(self.seconds)
            # NOTE: implement asyncio.Event to cancel the timer
            await self.handler(*args, **kwargs)
            if not self.repeat:
                break


class LoopWrapper(ABCLoopWrapper):
    def __init__(
        self,
        tasks: list[CoroutineTask] | None = None,
        error_handlers: dict[type[BaseException], list[ErrorHandler]] | None = None,
    ):
        self._loop = asyncio.new_event_loop()
        self.on_startup: list[CoroutineTask] = []
        self.on_shutdown: list[CoroutineTask] = []
        self.tasks = tasks or []
        self.error_handlers = error_handlers or DEFAULT_ERROR_HANDLERS
        
    def run_error_handler(self, exception: BaseException) -> None:
        handlers = self.error_handlers.get(exception.__class__)
        if not handlers:
            return
        for handler in handlers:
            try:
                self._loop.run_until_complete(handler(exception))
            except BaseException as exc:
                logger.error(
                    "Exception {!r} occurred during running error handler {!r} "
                    "in loop wrapper.",
                    exc.__class__.__name__,
                    handler.__name__,
                )
    
    def run(self) -> None:
        if not self.tasks:
            logger.warning("You ran loop with 0 tasks. Is it ok?")

        for startup_task in self.on_startup:
            self._loop.run_until_complete(startup_task)
        for task in self.tasks:
            self._loop.create_task(task)

        try:
            self.run_event_loop(asyncio.all_tasks(self._loop))
        except BaseException as exc:
            if self.error_handlers:
                self.run_error_handler(exc)
            self.complete_tasks()
        finally:
            for shutdown_task in self.on_shutdown:
                self._loop.run_until_complete(shutdown_task)
            if self._loop.is_running():
                self._loop.close()
        

    def run_event_loop(self, tasks: set[asyncio.Task[typing.Any]]) -> None:
        while tasks:
            tasks_results, _ = self._loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            )
            for task_result in tasks_results:
                try:
                    task_result.result()
                except BaseException as ex:
                    logger.exception(ex)
            tasks = asyncio.all_tasks(self._loop)

    def add_task(self, task: CoroutineFunc | CoroutineTask | DelayedTask):
        if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
            task = task()
        elif not asyncio.iscoroutine(task):
            raise TypeError("Task should be coroutine or coroutine function.")

        if self._loop and self._loop.is_running():
            self._loop.create_task(task)
        else:
            self.tasks.append(task)
    
    def complete_tasks(self, *tasks: asyncio.Task[typing.Any]) -> None:
        tasks = set(tasks) | asyncio.all_tasks(self._loop)  # type: ignore
        task_to_cancel = asyncio.gather(*tasks)
        task_to_cancel.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            self._loop.run_until_complete(task_to_cancel)

    def timer(
        self,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: float = 0,
        repeat: bool = False,
    ) -> typing.Callable[[typing.Callable], typing.Callable]:
        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: typing.Callable):
            self.add_task(DelayedTask(
                func,
                seconds,
                repeat=repeat,
            ))
            return func

        return decorator
    