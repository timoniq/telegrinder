from __future__ import annotations

import asyncio
import contextlib
import datetime
import enum
import signal
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


def sigint_handler(loop_wrapper: LoopWrapper) -> None:
    try:
        print(flush=True)
        logger.info("Caught KeyboardInterrupt, stopping loop wrapper...")
        loop_wrapper.stop()
    finally:
        raise KeyboardInterrupt


class DelayedFunction[**P, R](typing.Protocol):
    __name__: str
    __delayed_task__: DelayedTask[typing.Callable[P, CoroutineTask[R]]]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> CoroutineTask[R]: ...

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
    _future_tasks: list[CoroutineTask[typing.Any]]
    _state: LoopWrapperState
    _all_tasks: set[asyncio.Task[typing.Any]]
    _limit: int | None
    _semaphore: asyncio.Semaphore | None
    _event_stop: asyncio.Event

    __slots__ = (
        "_loop",
        "_lifespan",
        "_future_tasks",
        "_state",
        "_all_tasks",
        "_limit",
        "_semaphore",
        "_handle_run_async_event_loop",
        "_event_stop",
    )

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._event_stop = asyncio.Event()
        self._lifespan = Lifespan()
        self._future_tasks = [self._waiter_stop()]
        self._state = LoopWrapperState.NOT_RUNNING
        self._all_tasks = set()
        self._limit = None
        self._semaphore = None
        self._soon_run_event_loop()

    def __call__(self) -> asyncio.AbstractEventLoop:
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
        await logger.adebug("Running loop wrapper")

        while self._future_tasks:
            await self.create_task(self._future_tasks.pop(0))

        self.loop.add_signal_handler(signal.SIGINT, sigint_handler, self)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        if hasattr(signal, "SIGBREAK"):
            self.loop.add_signal_handler(signal.SIGBREAK, self.stop)

        while self.running and (tasks := self._get_all_tasks()):
            tasks_results, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            for task_result in tasks_results:
                try:
                    task_result.result()
                except Exception:
                    await logger.aexception("Traceback message below:")

    async def _cancel_tasks(self) -> None:
        try:
            await cancel_future(asyncio.gather(*self._get_all_tasks(), return_exceptions=True))
        except asyncio.exceptions.CancelledError:
            return

    @contextlib.asynccontextmanager
    async def _async_wrap_loop(self) -> typing.AsyncGenerator[typing.Any, None]:
        try:
            try:
                await self._lifespan._start()
            finally:
                yield
        except asyncio.CancelledError:
            if self.running:
                await self._cancel_tasks()
        finally:
            await self._shutdown(shutdown_lifespan=self.running)

    async def _shutdown(self, shutdown_lifespan: bool = True) -> None:
        if shutdown_lifespan:
            await self.lifespan._shutdown(None, None, None)
        await logger.adebug("Shutting down loop wrapper")
        self._state = LoopWrapperState.SHUTDOWN

    async def _waiter_stop(self) -> None:
        await self._event_stop.wait()
        self._state = LoopWrapperState.SHUTDOWN
        self._event_stop.clear()
        await self._shutdown()
        await self._cancel_tasks()

    async def _run_coro_with_semaphore(self, coro: CoroutineTask[typing.Any], /) -> None:
        assert self._semaphore is not None
        try:
            await coro
        finally:
            self._semaphore.release()

    async def _create_task_with_semaphore(self, coro: CoroutineTask[typing.Any], /) -> None:
        assert self._semaphore is not None
        await self._semaphore.acquire()
        self._create_task(self._run_coro_with_semaphore(coro))

    def _soon_run_event_loop(self) -> None:
        self._handle_run_async_event_loop = self._loop.call_soon_threadsafe(
            callback=lambda: self._loop.create_task(self._run_async_event_loop()),
        )

    def _create_task[T](self, coro: CoroutineTask[T], /) -> asyncio.Task[T]:
        task = self._loop.create_task(coro)
        self._all_tasks.add(task)
        task.add_done_callback(self._all_tasks.discard)
        return task

    def _get_all_tasks(self) -> Tasks:
        """Get a set of all tasks from the loop wrapper and event loop (`exclude the current task if any`)."""

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
            try:
                self.lifespan.start()
            finally:
                yield
        except KeyboardInterrupt:
            if self.running:
                run_task(self._cancel_tasks(), loop=self._loop)
        finally:
            if self.running:
                run_task(self._shutdown(shutdown_lifespan=self.running), loop=self._loop)
            else:
                logger.debug("Loop wrapper stopped")

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

    @property
    def tasks_limit(self) -> int | None:
        return self._limit

    def run(self, *, close_loop: bool = True) -> typing.NoReturn:  # type: ignore
        if self.running:
            raise RuntimeError("Loop wrapper already running.")

        self._state = LoopWrapperState.RUNNING_MANUALLY
        with self._wrap_loop(close_loop=close_loop):
            run_task(self._run(), loop=self._loop)

    def stop(self) -> None:
        if not self._event_stop.is_set():
            self._event_stop.set()

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
            self._handle_run_async_event_loop.cancel()
            self._soon_run_event_loop()

        return self

    def limit(self, value: int, /) -> typing.Self:
        if self._limit is not None:
            raise ValueError("Cannot reset limit value.")

        self._limit = value
        self._semaphore = asyncio.Semaphore(value)
        return self

    def add_task(self, task: Task[..., typing.Any], /) -> None:
        coro_task = to_coroutine_task(task)
        self._create_task(coro_task) if self.running else self._future_tasks.append(coro_task)

    async def create_task(self, task: Task[..., typing.Any], /) -> None:
        coro_task = to_coroutine_task(task)

        if not self.running:
            self._future_tasks.append(coro_task)
        elif self._semaphore is not None:
            await self._create_task_with_semaphore(coro_task)
        else:
            self._create_task(coro_task)

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

    if typing.TYPE_CHECKING:
        interval = timer

    else:

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
