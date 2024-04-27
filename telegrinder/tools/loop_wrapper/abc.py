import typing
from abc import ABC, abstractmethod


class ABCLoopWrapper(ABC):
    @abstractmethod
    def add_task(self, task: typing.Any) -> None:
        pass

    @abstractmethod
    def run_event_loop(self) -> None:
        pass


__all__ = ("ABCLoopWrapper",)
