import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.source import ChatSource, UserSource
from telegrinder.types.enums import ChatType, DiceEmoji

Message: typing.TypeAlias = MessageCute


class IsBot(ABCRule):
    def check(self, user: UserSource) -> bool:
        return user.is_bot


class IsUser(ABCRule):
    def check(self, user: UserSource) -> bool:
        return not user.is_bot


class IsPremium(ABCRule):
    def check(self, user: UserSource) -> bool:
        return user.is_premium.unwrap_or(False)


class IsLanguageCode(ABCRule):
    def __init__(self, lang_codes: str | list[str], /) -> None:
        self.lang_codes = [lang_codes] if isinstance(lang_codes, str) else lang_codes

    def check(self, user: UserSource) -> bool:
        return user.language_code.unwrap_or_none() in self.lang_codes


class IsUserId(ABCRule):
    def __init__(self, user_ids: int | list[int], /) -> None:
        self.user_ids = [user_ids] if isinstance(user_ids, int) else user_ids

    def check(self, user: UserSource) -> bool:
        return user.id in self.user_ids


class IsForum(ABCRule):
    def check(self, chat: ChatSource) -> bool:
        return chat.is_forum.unwrap_or(False)


class IsChatId(ABCRule):
    def __init__(self, chat_ids: int | list[int], /) -> None:
        self.chat_ids = [chat_ids] if isinstance(chat_ids, int) else chat_ids

    def check(self, chat: ChatSource) -> bool:
        return chat.id in self.chat_ids


class IsPrivate(ABCRule):
    def check(self, chat: ChatSource) -> bool:
        return chat.type == ChatType.PRIVATE


class IsGroup(ABCRule):
    def check(self, chat: ChatSource) -> bool:
        return chat.type == ChatType.GROUP


class IsSuperGroup(ABCRule):
    def check(self, chat: ChatSource) -> bool:
        return chat.type == ChatType.SUPERGROUP


class IsChat(ABCRule):
    def check(self, chat: ChatSource) -> bool:
        return chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)


class IsDice(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.dice)


class IsDiceEmoji(ABCRule, requires=[IsDice()]):
    def __init__(self, dice_emoji: DiceEmoji, /) -> None:
        self.dice_emoji = dice_emoji

    def check(self, message: Message) -> bool:
        return message.dice.unwrap().emoji == self.dice_emoji


class IsForward(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.forward_origin)


class IsForwardType(ABCRule, requires=[IsForward()]):
    def __init__(self, fwd_type: typing.Literal["user", "hidden_user", "chat", "channel"], /) -> None:
        self.fwd_type = fwd_type

    def check(self, message: Message) -> bool:
        return message.forward_origin.unwrap().v.type == self.fwd_type


class IsReply(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.reply_to_message)


class IsSticker(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.sticker)


class IsVideoNote(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.video_note)


class IsDocument(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.document)


class IsPhoto(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.photo)


__all__ = (
    "IsBot",
    "IsChat",
    "IsChatId",
    "IsDice",
    "IsDiceEmoji",
    "IsDocument",
    "IsForum",
    "IsForward",
    "IsForwardType",
    "IsGroup",
    "IsLanguageCode",
    "IsPhoto",
    "IsPremium",
    "IsPrivate",
    "IsReply",
    "IsSticker",
    "IsSuperGroup",
    "IsUser",
    "IsUserId",
    "IsVideoNote",
)
