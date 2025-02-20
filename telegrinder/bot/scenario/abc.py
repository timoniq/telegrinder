import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types.base import BaseCute

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch.view.abc import ABCStateView


class ABCScenario[Event: BaseCute](ABC):
    @abstractmethod
    def wait(self, api: "API", view: "ABCStateView[Event]") -> typing.Any:
        pass


__all__ = ("ABCScenario",)
