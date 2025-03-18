from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.waiter_machine.hasher.hasher import Hasher


class ABCScenario[Event: BaseCute](ABC):
    @abstractmethod
    def wait(self, hasher: Hasher, api: API) -> typing.Any:
        pass


__all__ = ("ABCScenario",)
