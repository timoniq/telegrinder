from .abc import ABC, Message, abstractmethod
from .markup import PatternLike, check_string
from .text import ABCTextMessageRule
import typing
import vbml


class ABCQuery(ABC):       
    @abstractmethod
    async def check(self, message: Message, query: str, ctx: dict) -> bool:
        ...


class StrQuery(ABCQuery):
    def __init__(self, value: str) -> None:
        self.value = value
    
    async def check(self, _: Message, query: str, ctx: dict) -> bool:
        if query == self.value:
            ctx.update({"start_query": self.value})
            return True
        return False


class IntQuery(ABCQuery):
    def __init__(self, value: int) -> None:
        self.value = value
    
    async def check(self, _: Message, query: str, ctx: dict) -> bool:
        if query.isdigit() and int(query) == self.value:
            ctx.update({"start_query": self.value})
            return True
        return False


class MarkupQuery(ABCQuery):
    def __init__(self, value: typing.Union[PatternLike, typing.List[PatternLike]]) -> None:
        if not isinstance(value, list):
            value = [value]
        self.value = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in value
        ]
    
    async def check(self, _: Message, query: str, ctx: dict) -> bool:
        markup_ctx = {}
        if check_string(self.value, query, markup_ctx):
            ctx.update({"start_query": markup_ctx})
            return True
        return False


class StartQuery(ABCTextMessageRule):
    def __init__(self, query: typing.Optional[ABCQuery] = None) -> None:
        self.query = query
    
    async def check(self, message: Message, ctx: dict) -> bool:
        if not message.text.startswith("/start "):
            return False
        query = message.text.lstrip("/start ")
        if self.query is None:
            ctx.update({"start_query": query})
            return True
        return await self.query.check(message, query, ctx)
