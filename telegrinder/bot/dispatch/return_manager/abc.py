import dataclasses
import inspect
from abc import ABC, abstractmethod
from annotationlib import Format
from functools import cached_property

import typing_extensions as typing
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


def register_manager(
    return_type: typing.TypeForm[typing.Any],
    /,
    *,
    agent_cls: type[Agent] = EventLoopAgent,
) -> typing.Callable[[ManagerFunction], Manager]:
    def wrapper(function: ManagerFunction, /) -> Manager:
        return Manager(_get_types(return_type), function, agent_cls=agent_cls)

    return wrapper


@dataclasses.dataclass
class Manager:
    types: tuple[typing.Any, ...]
    function: ManagerFunction
    agent_cls: type[Agent] = EventLoopAgent

    def __post_init__(self) -> None:
        if not self.types:
            raise ValueError("`Manager` must have at least one type.")

        self._types = frozenset(self.types)
        self._has_any_type = typing.Any in self._types
        self._sig = inspect.signature(self.function, annotation_format=Format.STRING)
        self._handler_response_required = "handler_response" in self._sig.parameters

    async def __call__(self, response: typing.Any, context: Context) -> None:
        if self._handler_response_required:
            context = context.copy()
            context.handler_response = response

        async with compose(
            self.function,
            context,
            agent_cls=self.agent_cls,
        ) as result:
            match result:
                case Error(error):
                    logger.debug(
                        "Return manager `{}` failed with error:{}",
                        fullname(self.function),
                        NodeError(f"failed to compose return manager `{fullname(self.function)}`", from_error=error),
                    )

    def check_respose_type(self, response_type: typing.TypeForm[typing.Any], /) -> bool:
        return self._has_any_type or response_type in self._types


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
        return "<{}: managers={!r}>".format(fullname(self), self.managers)

    @cached_property
    def managers(self) -> list[Manager]:
        return [manager for manager in vars(type(self)).values() if isinstance(manager, Manager)]

    async def run(
        self,
        response: typing.Any,
        api: API,
        update: Update,
        context: Context,
    ) -> None:
        response_type = type(response)

        for manager in self.managers:
            if manager.check_respose_type(response_type):
                logger.debug(
                    "Running manager `{}` for response of type `{}`",
                    fullname(manager.function),
                    fullname(response),
                )
                await manager(response, context)

    def register_manager(
        self,
        return_type: typing.TypeForm[typing.Any],
        /,
        *,
        agent_cls: type[Agent] = EventLoopAgent,
    ) -> typing.Callable[[ManagerFunction], Manager]:
        def wrapper(function: ManagerFunction, /) -> Manager:
            self.managers.append(manager := register_manager(return_type, agent_cls=agent_cls)(function))
            return manager

        return wrapper


__all__ = (
    "ABCReturnManager",
    "BaseReturnManager",
    "Manager",
    "register_manager",
)
