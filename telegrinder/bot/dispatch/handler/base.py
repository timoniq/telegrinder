import abc
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.rules.abc import ABCRule


class BaseReplyHandler(FuncHandler, abc.ABC):
    final: bool

    def __init__(
        self,
        *rules: ABCRule,
        final: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.as_reply = as_reply
        self.default_params = default_params
        super().__init__(
            function=self.handle,
            rules=list(rules),
            final=final,
            preset_context=preset_context or Context(),
        )

    @abc.abstractmethod
    async def handle(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        pass


__all__ = ("BaseReplyHandler",)
