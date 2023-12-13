import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute

if typing.TYPE_CHECKING:
    from telegrinder.api import ABCAPI
    from telegrinder.bot.dispatch.view.abc import ABCStateView


class ABCScenario(ABC):
    @abstractmethod
    def wait(self, api: "ABCAPI", dispatch: "ABCStateView[CallbackQueryCute]") -> typing.Any:
        pass
