import typing

from telegrinder.bot.cute_types import MessageCute

from .abc import ABCReturnManager, Manager, get_union_types

T = typing.TypeVar("T")


class MessageReturnManager(ABCReturnManager[MessageCute]):
    def __init__(self) -> None:
        self.managers: list[Manager] = []
        self.managers.extend(self.collect_managers())
    
    @staticmethod
    async def str_manager(value: str, event: MessageCute, ctx: dict) -> None:
        await event.answer(value)
    
    @staticmethod
    async def seq_manager(value: list[str] | tuple[str, ...], event: MessageCute, ctx: dict) -> None:
        for message in value:
            await event.answer(message)
    
    @staticmethod
    async def dict_manager(value: dict, event: MessageCute, ctx: dict) -> None:
        await event.answer(**value)

    def register(
        self, return_type: type[T]
    ) -> typing.Callable[[typing.Callable[[T, MessageCute, dict], typing.Awaitable]], Manager]:
        def wrapper(func: typing.Callable):
            manager = Manager(get_union_types(return_type) or (return_type,), func)
            self.managers.append(manager)
            return manager
        
        return wrapper
    
    async def run(self, value: typing.Any, event: MessageCute, context: dict) -> None:
        for manager in self.managers:
            if typing.Any in manager.types or any(type(value) is x for x in manager.types):
                await manager(value, event, context)
