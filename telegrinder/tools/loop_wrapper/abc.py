import typing
from abc import ABC, abstractmethod


class ABCLoopWrapper(ABC):
    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass

    @abstractmethod
    def add_task(self, task: typing.Any, /) -> None:
        pass

    @abstractmethod
    def run_event_loop(self) -> typing.NoReturn:
        raise NotImplementedError


__all__ = ("ABCLoopWrapper",)
