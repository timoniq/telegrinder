import dataclasses
import types
import typing
from abc import ABC, abstractmethod
from collections import OrderedDict

from telegrinder.bot.cute_types import BaseCute
from telegrinder.modules import logger

T = typing.TypeVar("T")
EventT = typing.TypeVar("EventT", bound=BaseCute, contravariant=True)


def get_union_types(t: typing.Any) -> tuple[type, ...] | None:
    if type(t) in (types.UnionType, typing._UnionGenericAlias):  # type: ignore
        return tuple(typing.get_origin(x) or x for x in typing.get_args(t))
    return None


def register_manager(return_type: type):
    def wrapper(func: typing.Callable[..., typing.Awaitable]):
        return Manager(get_union_types(return_type) or (return_type,), func)
    
    return wrapper


class ReturnContext(OrderedDict[str, typing.Any]):
    """`ReturnContext` class is used to pass the context from the handler using return manager.
    
    ```
    @bot.on.message(Markup("/say <text>"), is_blocking=False)
    async def handler(message: Message, text: str) -> Context:
        # some code...
        return ReturnContext(user=User(...))
    
    @bot.on.message(IsPrivate())
    async def next_handler(message: Message, user: User):
        ...
    ```
    """


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
    async def run(self, response: typing.Any, event: EventT, ctx: dict) -> None:
        pass


class BaseReturnManager(ABCReturnManager[EventT]):
    @property
    def managers(self) -> list[Manager]:
        return [
            manager
            for manager in (vars(BaseReturnManager) | vars(self.__class__)).values()
            if isinstance(manager, Manager)
        ]

    @register_manager(ReturnContext)
    @staticmethod
    async def ctx_manager(value: ReturnContext, event: EventT, ctx: dict) -> None:
        """Basic manager for returning context from handler."""
        
        ctx.update(value)
    
    async def run(self, response: typing.Any, event: EventT, ctx: dict) -> None:
        for manager in self.managers:
            if typing.Any in manager.types or any(type(response) is x for x in manager.types):
                await manager(response, event, ctx)

    def register(self, return_type: type[T]):
        def wrapper(func: typing.Callable[[T, EventT, dict], typing.Awaitable]) -> Manager:
            manager = Manager(get_union_types(return_type) or (return_type,), func)
            setattr(self.__class__, func.__name__, manager)
            return manager
        
        return wrapper
