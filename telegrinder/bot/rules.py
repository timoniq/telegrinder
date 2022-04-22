from abc import ABC, abstractmethod
import typing
import vbml

T = typing.TypeVar("T")
patcher = vbml.Patcher()

AnyDataclass = 0x00_01


class ABCRule(ABC, typing.Generic[T]):
    __dataclass__ = AnyDataclass

    @abstractmethod
    async def check(self, event: T, ctx: dict) -> bool:
        pass

    def __and__(self, other: "ABCRule"):
        return AndRule(self, other)

    def __or__(self, other: "ABCRule"):
        return OrRule(self, other)


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: T, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        r = all((await rule.check(event, ctx_copy)) for rule in self.rules)
        if not r:
            return False
        ctx.clear()
        ctx.update(ctx_copy)
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: T, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        r = any([(await rule.check(event, ctx_copy)) for rule in self.rules])
        if not r:
            return False
        ctx.clear()
        ctx.update(ctx_copy)
        return True


class IsMessage(ABCRule):
    __dataclass__ = dict

    async def check(self, event: dict, ctx: dict) -> bool:
        return "message" in event


class Text(ABCRule):
    __dataclass__ = dict

    def __init__(
        self,
        texts: typing.Union[str, typing.List[str]],
        ignore_case: bool = False
    ):
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts
        self.ignore_case = ignore_case

    async def check(self, event: dict, ctx: dict) -> bool:
        if self.ignore_case:
            return event["message"].get("text", "").lower() in list(map(str.lower, self.texts))
        return event["message"].get("text", "") in self.texts


class IsPrivate(ABCRule):
    __dataclass__ = dict

    async def check(self, event: T, ctx: dict) -> bool:
        return event["message"]["chat"]["id"] > 0


class IsChat(ABCRule):
    __dataclass__ = dict

    async def check(self, event: T, ctx: dict) -> bool:
        return event["message"]["chat"]["id"] < 0


class Markup(ABCRule):
    __dataclass__ = dict

    def __init__(self, patterns: typing.Union[str, typing.List[str]]):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, event: dict, ctx: dict) -> bool:
        for pattern in self.patterns:
            response = patcher.check(pattern, event["message"]["text"])
            if response is False:
                continue
            ctx.update(response)
            return True
        return False


class FuncRule(ABCRule, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable[[T, dict], bool],
        dataclass: typing.Optional[typing.Type[T]] = None
    ):
        self.func = func
        self.dataclass = dataclass

    async def check(self, event: dict, ctx: dict) -> bool:
        return self.func(self.dataclass(**event) if self.dataclass else event, ctx)



__all__ = (
    ABCRule,
    AndRule,
    OrRule,
    IsMessage,
    Text,
    Markup,
    IsPrivate,
    IsChat,
    FuncRule,
)
