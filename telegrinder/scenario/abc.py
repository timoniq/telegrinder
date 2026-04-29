import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
    from telegrinder.bot.dispatch.view.abc import ABCView
    from telegrinder.tools.waiter_machine.hasher.hasher import Hasher


class ABCScenario(ABC):
    @abstractmethod
    async def wait(
        self,
        api: API,
        hasher: Hasher,
        *,
        view: ABCView | None = None,
        waiter_middleware: WaiterMiddleware | None = None,
    ) -> typing.Any:
        pass


__all__ = ("ABCScenario",)
