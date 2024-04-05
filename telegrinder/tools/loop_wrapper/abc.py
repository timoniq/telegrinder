import typing
from abc import ABC, abstractmethod

CoroutineTask: typing.TypeAlias = typing.Coroutine[typing.Any, typing.Any, typing.Any]
CoroutineFunc: typing.TypeAlias = typing.Callable[..., CoroutineTask]


class ABCLoopWrapper(ABC):
    @abstractmethod
    def add_task(self, task: CoroutineFunc | CoroutineTask) -> None:
        pass

    @abstractmethod
    def run_event_loop(self) -> None:
        pass


__all__ = ("ABCLoopWrapper",)
