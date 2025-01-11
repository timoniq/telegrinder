import asyncio
import dataclasses
import typing

type CoroutineTask[T] = typing.Coroutine[typing.Any, typing.Any, T]
type CoroutineFunc[**P, T] = typing.Callable[P, CoroutineTask[T]]
type Task[**P, T] = CoroutineFunc[P, T] | CoroutineTask[T] | DelayedTask[typing.Callable[P, CoroutineTask[T]]]


def run_tasks(
    tasks: list[CoroutineTask[typing.Any]],
) -> None:
    loop = asyncio.get_event_loop()
    while tasks:
        loop.run_until_complete(tasks.pop(0))


def to_coroutine_task(task: Task) -> CoroutineTask[typing.Any]:
    if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
        task = task()
    elif not asyncio.iscoroutine(task):
        raise TypeError("Task should be coroutine or coroutine function.")
    return task


@dataclasses.dataclass(slots=True)
class DelayedTask[CoroFunc: CoroutineFunc[..., typing.Any]]:
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

    def start(self) -> None:
        run_tasks(self.startup_tasks)

    def shutdown(self) -> None:
        run_tasks(self.shutdown_tasks)

    def __enter__(self) -> None:
        self.start()

    def __exit__(self) -> None:
        self.shutdown()

    async def __aenter__(self) -> None:
        for task in self.startup_tasks:
            await task

    async def __aexit__(self, *args) -> None:
        for task in self.shutdown_tasks:
            await task

    def __add__(self, other: "Lifespan") -> "Lifespan":
        return Lifespan(
            startup_tasks=self.startup_tasks + other.startup_tasks,
            shutdown_tasks=self.shutdown_tasks + other.shutdown_tasks,
        )


__all__ = (
    "CoroutineTask",
    "DelayedTask",
    "Lifespan",
    "run_tasks",
    "to_coroutine_task",
)
