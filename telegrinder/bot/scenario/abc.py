from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.dispatch.view.abc import ABCView
    from telegrinder.bot.dispatch.waiter_machine.hasher.hasher import Hasher


class ABCScenario(ABC):
    @abstractmethod
    def wait(self, hasher: Hasher, view: ABCView, api: API) -> typing.Any:
        pass


__all__ = ("ABCScenario",)
