from abc import ABC, abstractmethod


class ABCBackoff(ABC):
    @abstractmethod
    def compute(self, failures: int) -> float:
        pass


__all__ = ("ABCBackoff",)
