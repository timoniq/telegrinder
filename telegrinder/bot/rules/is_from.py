import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.msgspec_utils import Option
from telegrinder.types.enums import ChatType, DiceEmoji
from telegrinder.types.objects import User

from .abc import ABCRule, Message, MessageRule

T = typing.TypeVar("T", bound=BaseCute)


@typing.runtime_checkable
class FromUserProto(typing.Protocol):
    from_: User | Option[User]


class HasFrom(ABCRule[T]):
    async def check(self, event: T, ctx: Context) -> bool:
        return isinstance(event, FromUserProto) and bool(event.from_)


class HasDice(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.dice)


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


class IsBot(MessageRule, requires=[HasFrom()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.from_user.is_bot


class IsUser(MessageRule, requires=[HasFrom()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return not message.from_user.is_bot


class IsPremium(MessageRule, requires=[HasFrom()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.from_user.is_premium.unwrap_or(False)


class IsLanguageCode(MessageRule, requires=[HasFrom()]):
    def __init__(self, lang_codes: str | list[str], /) -> None:
        self.lang_codes = [lang_codes] if isinstance(lang_codes, str) else lang_codes

    async def check(self, message: Message, ctx: Context) -> bool:
        if not message.from_user.language_code:
            return False
        return message.from_user.language_code.unwrap() in self.lang_codes


class IsForum(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.is_forum.unwrap_or(False)


class IsUserId(MessageRule, requires=[HasFrom()]):
    def __init__(self, user_ids: int | list[int], /) -> None:
        self.user_ids = [user_ids] if isinstance(user_ids, int) else user_ids

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.from_user.id in self.user_ids


class IsChatId(MessageRule):
    def __init__(self, chat_ids: int | list[int], /) -> None:
        self.chat_ids = [chat_ids] if isinstance(chat_ids, int) else chat_ids

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.id in self.chat_ids


class IsPrivate(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.type == ChatType.PRIVATE


class IsGroup(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.type == ChatType.GROUP


class IsSuperGroup(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.type == ChatType.SUPERGROUP


class IsChat(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)


class IsDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.DICE


class IsDartDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.DART


class IsBasketballDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.BASKETBALL


class IsFootballDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.FOOTBALL


class IsSlotMachineDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.SLOT_MACHINE


class IsBowlingDice(MessageRule, requires=[HasDice()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == DiceEmoji.BOWLING


__all__ = (
    "IsBasketballDice",
    "IsBot",
    "IsBowlingDice",
    "IsChat",
    "IsChatId",
    "IsDartDice",
    "IsDice",
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
