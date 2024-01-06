from telegrinder.bot.dispatch.context import Context
from telegrinder.types.enums import ChatType

from .abc import Message, MessageRule


class HasFrom(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.from_)


class IsReply(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.reply_to_message)


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
        return message.from_user.language_code.unwrap_or_none() in self.lang_codes


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
