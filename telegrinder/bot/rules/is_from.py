import typing

from fntypes.co import Nothing, Some

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.msgspec_utils import Option
from telegrinder.types.enums import ChatType, DiceEmoji
from telegrinder.types.objects import User

from .abc import ABCRule, Message
from .message import MessageRule

T = typing.TypeVar("T", bound=BaseCute)


def get_from_user(obj: typing.Any) -> User:
    assert isinstance(obj, FromUserProto)
    return obj.from_.unwrap() if isinstance(obj.from_, Some | Nothing) else obj.from_


@typing.runtime_checkable
class FromUserProto(typing.Protocol):
    from_: User | Option[User]


class HasFrom(ABCRule[T]):
    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        event_model = event.incoming_update.unwrap()
        return isinstance(event_model, FromUserProto) and bool(event_model.from_)


class HasDice(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.dice)


class IsForward(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.forward_origin)


class IsForwardType(MessageRule, requires=[IsForward()]):
    def __init__(
        self, fwd_type: typing.Literal["user", "hidden_user", "chat", "channel"], /
    ) -> None:
        self.fwd_type = fwd_type

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.forward_origin.unwrap().v.type == self.fwd_type


class IsReply(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.reply_to_message)


class IsSticker(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.sticker)


class IsBot(ABCRule[T], requires=[HasFrom()]):
    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return get_from_user(event.incoming_update.unwrap()).is_bot


class IsUser(ABCRule[T], requires=[HasFrom()]):
    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return not get_from_user(event.incoming_update.unwrap()).is_bot


class IsPremium(ABCRule[T], requires=[HasFrom()]):
    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return get_from_user(event.incoming_update.unwrap()).is_premium.unwrap_or(False)


class IsLanguageCode(ABCRule[T], requires=[HasFrom()]):
    def __init__(self, lang_codes: str | list[str], /) -> None:
        self.lang_codes = [lang_codes] if isinstance(lang_codes, str) else lang_codes

    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return (
            get_from_user(event.incoming_update.unwrap()).language_code.unwrap_or_none()
            in self.lang_codes
        )


class IsForum(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.chat.is_forum.unwrap_or(False)


class IsUserId(ABCRule[T], requires=[HasFrom()]):
    def __init__(self, user_ids: int | list[int], /) -> None:
        self.user_ids = [user_ids] if isinstance(user_ids, int) else user_ids

    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return get_from_user(event.incoming_update.unwrap()).id in self.user_ids


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


class IsDiceEmoji(MessageRule, requires=[HasDice()]):
    def __init__(self, dice_emoji: DiceEmoji, /) -> None:
        self.dice_emoji = dice_emoji

    async def check(self, message: Message, ctx: Context) -> bool:
        return message.dice.unwrap().emoji == self.dice_emoji


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
