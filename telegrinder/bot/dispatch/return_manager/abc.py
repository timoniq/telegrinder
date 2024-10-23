import dataclasses
import types
import typing
from abc import ABC, abstractmethod

from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.modules import logger


def get_union_types(t: types.UnionType | typing.Any) -> tuple[type[typing.Any], ...] | None:
    if type(t) in (types.UnionType, typing._UnionGenericAlias):  # type: ignore
        return tuple(typing.get_origin(x) or x for x in typing.get_args(t))
    return None


def register_manager(return_type: type[typing.Any] | types.UnionType):
    def wrapper(func: typing.Callable[..., typing.Awaitable[typing.Any]]):
        return Manager(get_union_types(return_type) or (return_type,), func)  # type: ignore

    return wrapper


@dataclasses.dataclass(frozen=True, slots=True)
class Manager:
    types: tuple[type, ...]
    callback: typing.Callable[..., typing.Awaitable[typing.Any]]

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        await self.callback(*args, **kwargs)


class ABCReturnManager[Event: Model](ABC):
    @abstractmethod
    async def run(self, response: typing.Any, event: Event, ctx: Context) -> None:
        pass


class BaseReturnManager[Event: Model](ABCReturnManager[Event]):
    def __repr__(self) -> str:
        return "<{}: {}>".format(
            self.__class__.__name__,
            ", ".join(x.callback.__name__ + "=" + repr(x) for x in self.managers),
        )

    @property
    def managers(self) -> list[Manager]:
        managers = self.__dict__.get("managers")
        if managers is not None:
            return managers
        managers_lst = [
            manager
            for manager in (vars(BaseReturnManager) | vars(self.__class__)).values()
            if isinstance(manager, Manager)
        ]
        self.__dict__["managers"] = managers_lst
        return managers_lst

    @register_manager(Context)
    @staticmethod
    async def ctx_manager(value: Context, event: Event, ctx: Context) -> None:
        """Basic manager for returning context from handler."""

        ctx.update(value)

    async def run(self, response: typing.Any, event: Event, ctx: Context) -> None:
        logger.debug("Run return manager for response: {!r}", response)
        for manager in self.managers:
            if typing.Any in manager.types or any(type(response) is x for x in manager.types):
                logger.debug("Run manager {!r}...", manager.callback.__name__)
                await manager(response, event, ctx)

    @typing.overload
    def register_manager[T](
        self,
        return_type: type[T],
    ) -> typing.Callable[[typing.Callable[[T, Event, Context], typing.Awaitable[typing.Any]]], Manager]: ...

    @typing.overload
    def register_manager[T](
        self,
        return_type: tuple[type[T], ...],
    ) -> typing.Callable[
        [typing.Callable[[tuple[T, ...], Event, Context], typing.Awaitable[typing.Any]]],
        Manager,
    ]: ...

    def register_manager[T](
        self,
        return_type: type[T] | tuple[type[T], ...],
    ) -> typing.Callable[
        [typing.Callable[[T | tuple[T, ...], Event, Context], typing.Awaitable[typing.Any]]],
        Manager,
    ]:
        def wrapper(func: typing.Callable[[T, Event, Context], typing.Awaitable]) -> Manager:
            manager = Manager(get_union_types(return_type) or (return_type,), func)  # type: ignore
            self.managers.append(manager)
            return manager

        return wrapper


__all__ = (
    "ABCReturnManager",
    "BaseReturnManager",
    "Manager",
    "get_union_types",
    "register_manager",
)
