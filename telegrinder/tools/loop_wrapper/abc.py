import typing
from abc import ABC, abstractmethod

CoroutineTask = typing.Coroutine[typing.Any, typing.Any, typing.Any]
CoroutineFunc = typing.Callable[..., CoroutineTask]


class ABCLoopWrapper(ABC):
    @abstractmethod
    def add_task(self, task: CoroutineFunc | CoroutineTask) -> None:
        ...

    @abstractmethod
    def run(self) -> None:
        ...
