import asyncio
import contextlib
import datetime
import enum
import signal
import typing
from contextlib import suppress

from telegrinder.modules import logger
from telegrinder.tools.aio import TaskGroup, cancel_future, loop_is_running, run_task
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

if typing.TYPE_CHECKING:
    from contextvars import Context

    type Tasks = set[asyncio.Task[typing.Any]]
    type DelayedFunctionDecorator[**P, R] = typing.Callable[[typing.Callable[P, R]], DelayedFunction[P, R]]

    class DelayedFunction[**P, R](typing.Protocol):
        __name__: str
        __delayed_task__: DelayedTask[typing.Callable[P, CoroutineTask[R]]]

        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> CoroutineTask[R]: ...

        def cancel(self) -> bool:
            """Cancel delayed task."""
            ...


class Timer(datetime.timedelta):
    repeat = False

    def __call__[**P, R](self, function: CoroutineFunc[P, R], /) -> DelayedFunction[P, R]:
        loop_wrapper = LoopWrapper()
        loop_wrapper.add_task(DelayedTask(function, seconds=self.total_seconds(), repeat=self.repeat))
        return function  # type: ignore


class Interval(Timer):
    repeat = True


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
    _event_stop: asyncio.Event
    _run_lw_task: asyncio.Handle
    _is_attached_to_running_loop: bool

    timer = Timer
    interval = Interval

    __slots__ = (
        "_lifespan",
        "_future_tasks",
        "_state",
        "_all_tasks",
        "_loop",
        "_event_stop",
        "_run_lw_task",
        "_is_attached_to_running_loop",
    )

    def __init__(self) -> None:
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()

        self._run_lw_task = self._run_lw_later()
        self._lifespan = Lifespan()
        self._event_stop = asyncio.Event()
        self._state = LoopWrapperState.NOT_RUNNING
        self._future_tasks = [self._waiter_stop()]
        self._all_tasks = set()
        self._is_attached_to_running_loop = False

        signal.signal(signal.SIGTERM, lambda *_: self.stop())

    def __repr__(self) -> str:
        return "<{}: loop={!r}, lifespan={!r}>".format(
            fullname(self) + (" (running)" if self.running else ""),
            self._loop,
            self._lifespan,
        )

    def __call__(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def lifespan(self) -> Lifespan:
        return self._lifespan

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def time(self) -> float:
        return self._loop.time()

    @property
    def running(self) -> bool:
        return self._state in {LoopWrapperState.RUNNING, LoopWrapperState.RUNNING_MANUALLY}

    @property
    def shutdown(self) -> bool:
        return self._state is LoopWrapperState.SHUTDOWN

    async def _run_async_event_loop(self) -> None:
        if not self.running:
            self._state = LoopWrapperState.RUNNING
            async with self._async_wrap_loop():
                await self._run()

    async def _run(self) -> None:
        await logger.adebug("Running loop wrapper")

        while self._future_tasks:
            self._create_task(self._future_tasks.pop(0))

        while self.running and (tasks := self._get_all_tasks()):
            tasks_results, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            for task_result in tasks_results:
                try:
                    task_result.result()
                except Exception:
                    await logger.aexception("Traceback message below:")

    async def _cancel_tasks(self) -> None:
        with suppress(asyncio.exceptions.CancelledError):
            await cancel_future(asyncio.gather(*self._get_all_tasks(), return_exceptions=True))

    @contextlib.asynccontextmanager
    async def _async_wrap_loop(self) -> typing.AsyncGenerator[typing.Any, None]:
        try:
            try:
                await self._lifespan._start()
            finally:
                yield
        except asyncio.CancelledError:
            await logger.adebug("Cancelling tasks...")
            await self._cancel_tasks()
        finally:
            await self._shutdown()

    async def _shutdown(self) -> None:
        await self.lifespan._shutdown(None, None, None)
        await logger.adebug("Shutting down loop wrapper")
        self._state = LoopWrapperState.SHUTDOWN

    async def _waiter_stop(self) -> None:
        await self._event_stop.wait()
        self._state = LoopWrapperState.SHUTDOWN
        self._event_stop.clear()
        await self._shutdown()
        await self._cancel_tasks()

    def _run_lw_later(self) -> asyncio.Handle:
        return self._loop.call_soon_threadsafe(lambda l: l.create_task(self._run_async_event_loop()), self._loop)

    def _create_task(
        self,
        coro: CoroutineTask[typing.Any],
        /,
        name: str | None = None,
        context: Context | None = None,
    ) -> asyncio.Task[typing.Any]:
        task = self._loop.create_task(coro, name=name, context=context)
        self._all_tasks.add(task)
        task.add_done_callback(self._all_tasks.discard)

        try:
            return task
        finally:
            del task

    def _get_all_tasks(self) -> Tasks:
        """Get a set of all tasks from the loop wrapper and event loop (`exclude the current task if any`)."""

        return (self._all_tasks | asyncio.all_tasks(loop=self._loop)).symmetric_difference(
            set() if (task := asyncio.current_task(self._loop)) is None else {task},
        )

    def _close_loop(self) -> None:
        if not self._loop.is_closed():
            logger.debug("Closing event loop {!r}", self._loop)
            self._loop.close()

    @contextlib.contextmanager
    def _wrap_loop(self, *, close_loop: bool = True) -> typing.Generator[typing.Any, None, None]:
        try:
            try:
                self.lifespan.start(self._loop)
            finally:
                yield
        except (KeyboardInterrupt, SystemExit) as e:
            print(flush=True)
            logger.info(f"Caught {e.__class__.__name__}, cancelling tasks")
            run_task(self._cancel_tasks(), loop=self._loop)

            if isinstance(e, SystemExit):
                raise
        finally:
            run_task(self._shutdown(), loop=self._loop)

            if close_loop:
                self._close_loop()

    def run(self, *, close_loop: bool = True) -> typing.NoReturn:  # type: ignore
        if self.running:
            raise RuntimeError("Loop wrapper already running.")

        self._state = LoopWrapperState.RUNNING_MANUALLY
        with self._wrap_loop(close_loop=close_loop):
            run_task(self._run(), loop=self._loop)

    def stop(self) -> None:
        if not self._event_stop.is_set():
            self._event_stop.set()

    def add_task(self, task: Task[..., typing.Any], /) -> None:
        coro_task = to_coroutine_task(task)

        if not self.running:
            self._future_tasks.append(coro_task)

            if self._is_attached_to_running_loop is False and loop_is_running():
                self.attach_to_running_loop()
        else:
            self._create_task(coro_task)

    def attach_to_running_loop(self) -> None:
        if self.running:
            raise RuntimeError("Cannot attach the running loop wrapper to the running loop.")

        self._loop = asyncio.get_running_loop()
        self._run_lw_task.cancel()
        self._is_attached_to_running_loop = True
        self._run_lw_task = self._run_lw_later()

    def create_task_group[T](self) -> TaskGroup[typing.Any]:
        loop = asyncio.get_running_loop()
        if not self.running and self._loop is not loop:
            self.attach_to_running_loop()
        return TaskGroup(loop)


__all__ = ("DelayedTask", "LoopWrapper", "to_coroutine_task")
