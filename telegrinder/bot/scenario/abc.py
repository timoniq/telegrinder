import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch import Dispatch


class ABCScenario(ABC):
    @abstractmethod
    def wait(self, api: "API", dispatch: "Dispatch") -> typing.Any:
        pass
