import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.is_from import IsPrivate
from telegrinder.bot.rules.markup import Markup
from telegrinder.bot.rules.message_entities import MessageEntities
from telegrinder.types.enums import MessageEntityType


class StartCommand(
    ABCRule,
    requires=[
        IsPrivate(),
        MessageEntities(MessageEntityType.BOT_COMMAND),
        Markup(["/start <param>", "/start"]),
    ],
):
    def __init__(
        self,
        validator: typing.Callable[[str], typing.Any | None] | None = None,
        *,
        param_required: bool = False,
        alias: str | None = None,
    ) -> None:
        self.param_required = param_required
        self.validator = validator
        self.alias = alias

    def check(self, ctx: Context) -> bool:
        param: str | None = ctx.pop("param", None)
        validated_param = self.validator(param) if self.validator and param is not None else param

        if self.param_required and validated_param is None:
            return False

        ctx.set(self.alias or "param", validated_param)
        return True


__all__ = ("StartCommand",)
