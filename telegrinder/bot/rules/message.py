import abc
import typing

from telegrinder.bot.adapter.event import EventAdapter
from telegrinder.types.objects import Message as MessageEvent

from .abc import ABCRule, CheckResult, Message


class MessageRule(ABCRule[Message], abc.ABC, adapter=EventAdapter(MessageEvent, Message)):
    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult: ...


__all__ = ("MessageRule",)
