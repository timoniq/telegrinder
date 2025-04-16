"""Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generate_noded models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement fields/methods/properties working only with model fields.
"""

from __future__ import annotations

from datetime import datetime
from functools import cached_property

from fntypes.option import Nothing, Option

from telegrinder.model import Model
from telegrinder.types import (
    Birthdate,
    Chat,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChatType,
    ContentType,
    DefaultAccentColor,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    UpdateType,
    User,
)


class _Birthdate(Birthdate):
    @property
    def is_birthday(self) -> bool:
        """True, if today is a user's birthday."""
        now = datetime.now()
        return now.month == self.month and now.day == self.day

    @property
    def age(self) -> Option[int]:
        """Optional. Contains the user's age, if the user has a birth year specified."""
        return self.year.map(lambda year: ((datetime.now() - datetime(year, self.month, self.day)) // 365).days)


class _Chat(Chat):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    @property
    def full_name(self) -> Option[str]:
        """Optional. Full name (`first_name` + `last_name`) of the
        other party in a `private` chat.
        """
        return self.first_name.map(lambda x: x + " " + self.last_name.unwrap_or(""))


class _ChatJoinRequest(ChatJoinRequest):
    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""
        return self.chat.id


class _ChatMemberUpdated(ChatMemberUpdated):
    @property
    def chat_id(self) -> int:
        """Alias `.chat_id` instead of `.chat.id`"""
        return self.chat.id


class _Message(Message):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.message_id == other.message_id and self.chat_id == other.chat_id

    @cached_property
    def content_type(self) -> ContentType:
        """Type of content that the message contains."""
        for content in ContentType:
            if content.value in self.__struct_fields__ and not isinstance(
                getattr(self, content.value, Nothing()),
                Nothing,
            ):
                return content
        return ContentType.UNKNOWN

    @property
    def from_user(self) -> "User":
        """`from_user` instead of `from_.unwrap()`."""
        return self.from_.unwrap()

    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""
        return self.chat.id

    @property
    def chat_title(self) -> str:
        """Chat title, for `supergroups`, `channels` and `group` chats.
        Full name, for `private` chat.
        """
        return self.chat.full_name.unwrap() if self.chat.type == ChatType.PRIVATE else self.chat.title.unwrap()


class _User(User):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    @property
    def default_accent_color(self) -> DefaultAccentColor:
        """User's or bot's accent color (non-premium)."""
        return DefaultAccentColor(self.id % 7)

    @property
    def full_name(self) -> str:
        """User's or bot's full name (`first_name` + `last_name`)."""
        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class _Update(Update):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.update_type == other.update_type

    @cached_property
    def update_type(self) -> UpdateType:
        """Incoming update type."""
        return UpdateType(
            next(
                (
                    x
                    for x in self.__struct_fields__
                    if x != "update_id" and not isinstance(getattr(self, x), Nothing)
                )
            ),
        )

    @cached_property
    def incoming_update(self) -> Model:
        """Incoming update."""
        return getattr(self, self.update_type.value).unwrap()


class _ReplyKeyboardMarkup(ReplyKeyboardMarkup):
    @property
    def empty_markup(self) -> ReplyKeyboardRemove:
        """Empty keyboard to remove the custom keyboard."""
        return ReplyKeyboardRemove(remove_keyboard=True, selective=self.selective.unwrap_or_none())
