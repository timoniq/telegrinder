import base64
import typing

import fntypes

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.is_from import IsPrivate
from telegrinder.bot.rules.markup import Markup
from telegrinder.node.me import BotUsername
from telegrinder.node.message_entities import MessageEntities
from telegrinder.types.enums import MessageEntityType


class StartCommand(
    ABCRule,
    requires=[
        IsPrivate(),
        Markup(
            [
                "/start <param>",
                "/start",
                "tg://resolve?domain=<bot_username>&start=<param>",
            ]
        ),
    ],
):
    def __init__(
        self,
        validator: typing.Callable[[str], typing.Any | None] | None = None,
        *,
        deep_link: bool | None = None,
        decode_deep_link_param: bool = False,
        param_required: bool = False,
        alias: str | None = None,
    ) -> None:
        self.param_required = param_required
        self.validator = validator
        self.alias = alias
        self.deep_link = deep_link
        self.decode_deep_link_param = decode_deep_link_param

    def check(
        self,
        bot_username: BotUsername,
        message_entities: fntypes.Option[MessageEntities],
        ctx: Context,
    ) -> bool:
        if self.deep_link is not None and all(
            (
                message_entities.map(
                    lambda entities: entities and entities[0].type == MessageEntityType.BOT_COMMAND,
                ).unwrap_or(False),
                self.deep_link and bot_username == ctx.get("bot_username"),
            ),
        ):
            return False

        param: str | None = ctx.pop("param", None)

        if param is not None and self.decode_deep_link_param:
            param = base64.urlsafe_b64decode(param.encode()).decode()

        validated_param = self.validator(param) if self.validator and param is not None else param

        if self.param_required and validated_param is None:
            return False

        ctx.set(self.alias or "param", validated_param)
        return True


__all__ = ("StartCommand",)
