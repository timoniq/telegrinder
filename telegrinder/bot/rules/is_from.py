import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.source import Source
from telegrinder.types.enums import ChatType, DiceEmoji

from .abc import ABCRule, Message
from .message import MessageRule


class HasDice(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.dice)


class IsBot(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.from_user.is_bot


class IsUser(ABCRule):
    async def check(self, source: Source) -> bool:
        return not source.from_user.is_bot


class IsPremium(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.from_user.is_premium.unwrap_or(False)


class IsLanguageCode(ABCRule):
    def __init__(self, lang_codes: str | list[str], /) -> None:
        self.lang_codes = [lang_codes] if isinstance(lang_codes, str) else lang_codes

    async def check(self, source: Source) -> bool:
        return source.from_user.language_code.unwrap_or_none() in self.lang_codes


class IsUserId(ABCRule):
    def __init__(self, user_ids: int | list[int], /) -> None:
        self.user_ids = [user_ids] if isinstance(user_ids, int) else user_ids

    async def check(self, source: Source) -> bool:
        return source.from_user.id in self.user_ids


class IsForum(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.chat.is_forum.unwrap_or(False)


class IsChatId(ABCRule):
    def __init__(self, chat_ids: int | list[int], /) -> None:
        self.chat_ids = [chat_ids] if isinstance(chat_ids, int) else chat_ids

    async def check(self, source: Source) -> bool:
        return source.chat.id in self.chat_ids


class IsPrivate(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.chat.type == ChatType.PRIVATE


class IsGroup(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.chat.type == ChatType.GROUP


class IsSuperGroup(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.chat.type == ChatType.SUPERGROUP


class IsChat(ABCRule):
    async def check(self, source: Source) -> bool:
        return source.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)


class IsDiceEmoji(MessageRule, requires=[HasDice()]):
    def __init__(self, dice_emoji: DiceEmoji, /) -> None:
        self.dice_emoji = dice_emoji

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == self.dice_emoji


class IsForward(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.forward_origin)


class IsForwardType(MessageRule, requires=[IsForward()]):
    def __init__(self, fwd_type: typing.Literal["user", "hidden_user", "chat", "channel"], /) -> None:
        self.fwd_type = fwd_type

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.forward_origin.unwrap().v.type == self.fwd_type


class IsReply(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.reply_to_message)


class IsSticker(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.sticker)


__all__ = (
    "IsBot",
    "IsChat",
    "IsChatId",
    "IsDiceEmoji",
    "IsForum",
    "IsForward",
    "IsForwardType",
    "IsGroup",
    "IsLanguageCode",
    "IsPremium",
    "IsPrivate",
    "IsReply",
    "IsSuperGroup",
    "IsUser",
    "IsUserId",
)
