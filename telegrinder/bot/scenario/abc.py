import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types.base import BaseCute

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch.view.abc import ABCStateView

EventT = typing.TypeVar("EventT", bound=BaseCute)


class ABCScenario(ABC, typing.Generic[EventT]):
    @abstractmethod
    def wait(self, api: "API", view: "ABCStateView[EventT]") -> typing.Any:
        pass


__all__ = ("ABCScenario",)
