from abc import ABC, abstractmethod


class KeyboardSetError(LookupError):
    pass


class KeyboardSetBase(ABC):
    @classmethod
    @abstractmethod
    def load(cls) -> None:
        pass


__all__ = ("KeyboardSetBase", "KeyboardSetError")
