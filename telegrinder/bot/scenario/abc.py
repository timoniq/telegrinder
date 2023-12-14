import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.callback_query import CallbackQueryCute

if typing.TYPE_CHECKING:
    from telegrinder.api import ABCAPI
    from telegrinder.bot.dispatch.view.abc import ABCStateView

EventT = typing.TypeVar("EventT", bound=BaseCute)


class ABCScenario(ABC, typing.Generic[EventT]):
    @abstractmethod
    def wait(self, api: "ABCAPI", view: "ABCStateView[EventT]") -> typing.Any:
        pass
