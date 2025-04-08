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
from telegrinder.tools.magic import cancel_future

type Tasks = set[asyncio.Task[typing.Any]]
type LoopFactory = typing.Callable[[], asyncio.AbstractEventLoop]
type DelayedFunctionDecorator[**P, R] = typing.Callable[[typing.Callable[P, R]], DelayedFunction[P, R]]

_NODEFAULT: typing.Final[object] = object()


class DelayedFunction[**P, R](typing.Protocol):
    __name__: str
    __delayed_task__: DelayedTask

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> typing.Coroutine[typing.Any, typing.Any, R]: ...

    def cancel(self) -> bool:
        """Cancel delayed task."""
        ...


class LoopWrapper:
    _loop: asyncio.AbstractEventLoop
    _lifespan: Lifespan
    _is_running: bool
    _close_loop: bool
    _tasks: list[CoroutineTask[typing.Any]]

    __singleton_instance__: typing.ClassVar[typing.Self | None] = None

    @typing.overload
    def __new__(cls) -> typing.Self: ...

    @typing.overload
    def __new__(cls, *, loop_factory: LoopFactory, close_loop: bool = ...) -> typing.Self: ...

    def __new__(
        cls,
        *,
        loop_factory: LoopFactory | None = None,
        close_loop: typing.Any = _NODEFAULT,
    ) -> typing.Self:
        loop_factory = loop_factory or asyncio.get_event_loop

        if cls.__singleton_instance__ is None:
            instance = super().__new__(cls)
            instance._loop = loop_factory()
            instance._lifespan = Lifespan()
            instance._is_running = False
            instance._close_loop = True if close_loop is _NODEFAULT else close_loop
            instance._tasks = []
            instance._loop.create_task(instance._run_inner())
            cls.__singleton_instance__ = instance
            return cls.__singleton_instance__

        if close_loop is not _NODEFAULT:
            cls.__singleton_instance__._close_loop = close_loop

        if cls.__singleton_instance__.is_running:
            if loop_factory is not None:
                logger.warning("The new factory was ignored, because the `LoopWrapper` is running.")
            return cls.__singleton_instance__

        loop = loop_factory()
        if loop is not cls.__singleton_instance__._loop:
            loop.create_task(cls.__singleton_instance__._run_inner())
            cls.__singleton_instance__._loop = loop

        return cls.__singleton_instance__

    def __call__(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def __repr__(self) -> str:
        return "<{}: loop={!r}{}, lifespan={!r}>".format(
            type(self).__name__,
            self._loop,
            " (running)" if self._is_running else "",
            self._lifespan,
        )

    @property
    def lifespan(self) -> Lifespan:
        return self._lifespan

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def is_running(self) -> bool:
        return self._is_running

    async def _run_inner(self) -> None:
        if self.is_running:
            return

        if not self.event_loop.is_running():
            return self.run()

        with self._handle_loop():
            async with self._lifespan:
                self._run_tasks()
                tasks = asyncio.all_tasks(loop=self._loop)
                while self._is_running and tasks:
                    tasks = self._handle_tasks_results(
                        (await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))[0],
                    )

    def _run(self) -> None:
        logger.debug("Running loop wrapper")
        self._is_running = True

    def _stop(self) -> None:
        logger.debug("Stopping loop wrapper")
        self._is_running = False

    def _run_tasks(self) -> None:
        if not self._is_running:
            return

        while self._tasks:
            self._loop.create_task(self._tasks.pop(0))

    def _handle_tasks_results(self, tasks: Tasks, /) -> Tasks:
        for task_result in tasks:
            try:
                if not task_result.cancelled() and (exception := task_result.exception()) is not None:
                    raise exception from None  # Raise the exception that was set on task.
            except BaseException:
                logger.exception("Traceback message below:")
            finally:
                tasks = asyncio.all_tasks(loop=self._loop)

        return tasks

    @contextlib.contextmanager
    def _handle_loop(self) -> typing.Generator[typing.Any, None, None]:
        try:
            self._run()
            yield
        except KeyboardInterrupt:
            print()  # Prints new line for ^C
            logger.info("Caught KeyboardInterrupt, cancellation tasks...")
            with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
                self._loop.run_until_complete(
                    future=cancel_future(
                        asyncio.gather(*asyncio.all_tasks(loop=self._loop), return_exceptions=True)
                    ),
                )
            self.lifespan.shutdown()
        finally:
            self._stop()
            if self._close_loop and not self._loop.is_running() and not self._loop.is_closed():
                logger.debug("Closing event loop {!r}", self._loop)
                self._loop.close()

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

    def run(self) -> typing.NoReturn:  # type: ignore
        if self.is_running:
            raise RuntimeError("Loop wrapper already running.")

        with self._handle_loop():
            self._lifespan.start()
            self._run_tasks()
            tasks = asyncio.all_tasks(loop=self._loop)
            while self._is_running and tasks:
                tasks = self._handle_tasks_results(
                    self._loop.run_until_complete(
                        future=asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION),
                    )[0],
                )

    def add_task(self, task: Task[..., typing.Any], /) -> None:
        coro = to_coroutine_task(task)
        if self.is_running:
            self._loop.create_task(coro)
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
    ) -> typing.Callable[..., typing.Any]:
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
    ) -> typing.Callable[..., typing.Any]:
        return self._get_delayed_task_decorator(
            repeat=True,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=delta or seconds,
        )


__all__ = ("DelayedTask", "LoopWrapper", "to_coroutine_task")
