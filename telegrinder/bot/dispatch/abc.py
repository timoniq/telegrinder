from abc import ABC, abstractmethod


class ABCDispatch(ABC):
    @abstractmethod
    def feed(self, event: dict) -> bool:
        pass
