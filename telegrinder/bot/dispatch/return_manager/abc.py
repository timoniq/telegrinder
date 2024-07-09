import dataclasses
import types
import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger

T = typing.TypeVar("T")
EventT = typing.TypeVar("EventT", bound=BaseCute, contravariant=True)


def get_union_types(t: types.UnionType) -> tuple[type, ...] | None:
    if type(t) in (types.UnionType, typing._UnionGenericAlias):  # type: ignore
        return tuple(typing.get_origin(x) or x for x in typing.get_args(t))
    return None


def register_manager(return_type: type[typing.Any] | types.UnionType):
    def wrapper(func: typing.Callable[..., typing.Awaitable[typing.Any]]):
        return Manager(get_union_types(return_type) or (return_type,), func)  # type: ignore

    return wrapper


@dataclasses.dataclass(frozen=True)
class Manager:
    types: tuple[type, ...]
    callback: typing.Callable[..., typing.Awaitable]

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        try:
            await self.callback(*args, **kwargs)
        except BaseException as ex:
            logger.exception(ex)


class ABCReturnManager(ABC, typing.Generic[EventT]):
    @abstractmethod
    async def run(self, response: typing.Any, event: EventT, ctx: Context) -> None:
        pass


class BaseReturnManager(ABCReturnManager[EventT]):
    def __repr__(self) -> str:
        return "<{}: {}>".format(
            self.__class__.__name__,
            ", ".join(x.callback.__name__ + "=" + repr(x) for x in self.managers),
        )

    @property
    def managers(self) -> list[Manager]:
        return [
            manager
            for manager in (vars(BaseReturnManager) | vars(self.__class__)).values()
            if isinstance(manager, Manager)
        ]

    @register_manager(Context)
    @staticmethod
    async def ctx_manager(value: Context, event: EventT, ctx: Context) -> None:
        """Basic manager for returning context from handler."""

        ctx.update(value)

    async def run(self, response: typing.Any, event: EventT, ctx: Context) -> None:
        logger.debug("Run return manager for response: {!r}", response)
        for manager in self.managers:
            if typing.Any in manager.types or any(type(response) is x for x in manager.types):
                logger.debug("Run manager {!r}...", manager.callback.__name__)
                await manager(response, event, ctx)

    @typing.overload
    def register_manager(
        self, return_type: type[T]
    ) -> typing.Callable[[typing.Callable[[T, EventT, Context], typing.Awaitable[typing.Any]]], Manager]: ...

    @typing.overload
    def register_manager(
        self,
        return_type: tuple[type[T], ...],
    ) -> typing.Callable[
        [typing.Callable[[tuple[T, ...], EventT, Context], typing.Awaitable[typing.Any]]],
        Manager,
    ]: ...

    def register_manager(
        self,
        return_type: type[T] | tuple[type[T], ...],
    ) -> typing.Callable[
        [typing.Callable[[T | tuple[T, ...], EventT, Context], typing.Awaitable[typing.Any]]],
        Manager,
    ]:
        def wrapper(func: typing.Callable[[T, EventT, Context], typing.Awaitable]) -> Manager:
            manager = Manager(get_union_types(return_type) or (return_type,), func)  # type: ignore
            setattr(self.__class__, func.__name__, manager)
            return manager

        return wrapper


__all__ = (
    "ABCReturnManager",
    "BaseReturnManager",
    "Manager",
    "get_union_types",
    "register_manager",
)
