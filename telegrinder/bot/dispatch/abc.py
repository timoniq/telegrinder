from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI


class ABCDispatch(ABC):
    @abstractmethod
    def feed(self, event: dict, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: "ABCDispatch"):
        pass
