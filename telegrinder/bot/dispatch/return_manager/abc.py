import dataclasses
import inspect
import types
import typing
from abc import ABC, abstractmethod
from collections import OrderedDict

from telegrinder.bot.cute_types import BaseCute
from telegrinder.modules import logger

T = typing.TypeVar("T")
Ts = typing.TypeVarTuple("Ts")
EventT = typing.TypeVar("EventT", bound=BaseCute, contravariant=True)


def get_union_types(union: typing.Any) -> tuple[type, ...] | None:
    if type(union) in (types.UnionType, typing._UnionGenericAlias):  # type: ignore
        return tuple(typing.get_origin(x) or x for x in typing.get_args(union))
    return None


def is_function_manager(func: typing.Callable) -> bool:
    if not inspect.iscoroutinefunction(func):
        return False

    signature = inspect.signature(func)
    params = list(signature.parameters.values())
    if len(params) != 3 or any(
        param.annotation is signature.empty
        for param in params[1:]
    ):
        return False
    
    for expected_annotation, param in zip((BaseCute, dict), params[1:]):
        if isinstance(param.annotation, typing.TypeVar):
            annotation = param.annotation.__bound__
        else:
            annotation = param.annotation
        
        if annotation is None or not issubclass(annotation, expected_annotation):
            return False
    
    return True


def get_manager_functions(cls: type["ABCReturnManager"]) -> list[typing.Callable[..., typing.Awaitable]]:
    return [
        obj.__func__
        for obj in cls.__dict__.values()
        if isinstance(obj, staticmethod)
        and is_function_manager(obj.__func__)
    ]


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
    @classmethod
    def collect_managers(cls) -> list[Manager]:
        """Сollection of static methods that serve as a function-manager.
        
        ```
        class SomeMessageReturnManager(ABCReturnManager[MessageCute]):
            @staticmethod
            async def manager(value: int, event: MessageCute, ctx: dict) -> None:
                ...
        
        >>> SomeMessageReturnManager.collect_managers()
        [Manager(types=(int,), callback=<function SomeMessageReturnManager.manager at 0x7f9cc1289da0>)]
        ```
        """

        if hasattr(cls, "__collected_managers__"):
            return getattr(cls, "__collected_managers__")
        
        functions = []
        managers = []

        for c in cls.mro():
            if issubclass(c, ABCReturnManager):
                functions.extend(get_manager_functions(c))

        for func in functions:
            signature = inspect.signature(func)
            value_type = list(signature.parameters.values())[0].annotation
            if value_type is signature.empty:
                value_type = (typing.Any,)
            else:
                value_type = get_union_types(value_type) or (value_type,)
            managers.append(Manager(value_type, func))

        setattr(cls, "__collected_managers__", managers)
        return managers
    
    @staticmethod
    async def ctx_manager(value: ReturnContext, event: EventT, ctx: dict) -> None:
        """Basic manager for returning context from handler."""
        
        ctx.update(value)

    @abstractmethod
    def register(
        self, return_type: type[T]
    ) -> typing.Callable[[typing.Callable[[T, EventT, dict], typing.Awaitable]], Manager]:
        ...

    @abstractmethod
    async def run(self, value: typing.Any, event: EventT, context: dict) -> None:
        pass
