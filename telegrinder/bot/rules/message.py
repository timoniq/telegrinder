import abc

from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Message as MessageEvent

from .abc import ABCRule, CheckResult, Message
from .adapter import EventAdapter


class MessageRule(ABCRule[Message], abc.ABC):
    adapter: EventAdapter[Message] = EventAdapter(MessageEvent, Message)

    @abc.abstractmethod
    def check(self, message: Message, ctx: Context) -> CheckResult: ...


__all__ = ("MessageRule",)
