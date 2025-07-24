from __future__ import annotations

import dataclasses
import typing
from abc import ABC, abstractmethod
from functools import cached_property

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.return_manager.utils import _get_types
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools import fullname
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

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

    @cached_property
    def required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.function, start_idx=1)

    async def __call__(
        self,
        response: typing.Any,
        update: Update,
        api: API,
        context: Context,
    ) -> None:
        data = {Update: update, API: api}
        node_col = None

        if self.required_nodes:
            match await compose_nodes(self.required_nodes, context, data=data):
                case Ok(value):
                    node_col = value
                case Error(compose_error):
                    logger.debug(
                        "Cannot compose nodes for return manager `{}`, error {!r}",
                        fullname(self.function),
                        compose_error.message,
                    )
                    return None

        temp_ctx = context.copy()
        try:
            bundle_function = bundle(self.function, {**data, Context: temp_ctx}, typebundle=True)
            bundle_function &= bundle(
                self.function,
                context | ({} if node_col is None else node_col.values),
            )
            await maybe_awaitable(bundle_function(response))
        finally:
            context |= temp_ctx
            # Closing per call node sessions if there are any
            if node_col is not None:
                await node_col.close_all()


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
            manager
            for manager in (vars(BaseReturnManager) | vars(type(self))).values()
            if isinstance(manager, Manager)
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
                logger.debug(
                    "Running manager `{}` for response `{!r}`",
                    fullname(manager.function),
                    response,
                )
                await manager(response, update, api, context)

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
