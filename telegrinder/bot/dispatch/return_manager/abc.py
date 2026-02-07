import dataclasses
import typing
from abc import ABC, abstractmethod
from functools import cached_property

from kungfu.library.monad.result import Error
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.error import NodeError

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.return_manager.utils import _get_types
from telegrinder.modules import logger
from telegrinder.node.compose import compose
from telegrinder.tools import fullname
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

type ManagerFunction = typing.Callable[..., typing.Any | typing.Awaitable[typing.Any]]


def register_manager(return_type: typing.Any, /) -> typing.Callable[[ManagerFunction], Manager]:
    def wrapper(function: ManagerFunction, /) -> Manager:
        function = function.__func__ if isinstance(function, classmethod | staticmethod) else function
        types = _get_types(return_type)
        return Manager((types,) if not isinstance(types, tuple) else types, function)

    return wrapper


@dataclasses.dataclass
class Manager:
    types: tuple[typing.Any, ...]
    function: ManagerFunction
    agent_cls: type[Agent] = EventLoopAgent

    async def __call__(self, response: typing.Any, context: Context) -> None:
        ctx = context.copy()
        ctx.handler_response = response

        async with compose(
            self.function,
            ctx,
            agent_cls=self.agent_cls,
        ) as result:
            match result:
                case Error(error):
                    await logger.adebug(
                        "Return manager `{}` failed with error:{}",
                        fullname(self.function),
                        NodeError(f"failed to compose return manager `{fullname(self.function)}`", from_error=error),
                    )


class ABCReturnManager(ABC):
    @property
    @abstractmethod
    def managers(self) -> list[Manager]:
        pass

    @abstractmethod
    async def run(self, response: typing.Any, api: API, update: Update, context: Context) -> None:
        pass


class BaseReturnManager(ABCReturnManager):
    def __repr__(self) -> str:
        return "<{}: {}>".format(fullname(self), self.managers)

    @cached_property
    def managers(self) -> list[Manager]:
        return [
            manager for manager in (vars(BaseReturnManager) | vars(type(self))).values() if isinstance(manager, Manager)
        ]

    async def run(
        self,
        response: typing.Any,
        api: API,
        update: Update,
        context: Context,
    ) -> None:
        for manager in self.managers:
            if typing.Any in manager.types or type(response) in manager.types:
                await logger.adebug(
                    "Running manager `{}` for response of type `{}`",
                    fullname(manager.function),
                    fullname(response),
                )
                await manager(response, context)

    def register_manager(self, return_type: typing.Any, /) -> typing.Callable[[ManagerFunction], Manager]:
        def wrapper(function: ManagerFunction, /) -> Manager:
            manager = register_manager(return_type)(function)
            self.managers.append(manager)
            return manager

        return wrapper


__all__ = (
    "ABCReturnManager",
    "BaseReturnManager",
    "Manager",
    "register_manager",
)
