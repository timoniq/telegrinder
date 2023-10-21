import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch import Dispatch  # noqa: I001
    from telegrinder.api import API  # noqa: I001


class ABCScenario(ABC):
    @abstractmethod
    def wait(self, api: "API", dispatch: "Dispatch") -> typing.Any:
        pass
