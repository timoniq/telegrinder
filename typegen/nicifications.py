"""
Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generate_noded models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement methods/properties working only with model fields.
"""

import typing
from datetime import datetime

from fntypes.option import Option, Some

from telegrinder.msgspec_utils import Nothing
from telegrinder.types import (
    Birthdate,
    Chat,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChatType,
    ContentType,
    DefaultAccentColor,
    InaccessibleMessage,
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

        return self.year.map(
            lambda year: ((datetime.now() - datetime(year, self.month, self.day)) // 365).days
        )


class _Chat(Chat):
    def __eq__(self, other: typing.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
        )

    @property
    def full_name(self) -> Option[str]:
        """Optional. Full name (`first_name` + `last_name`) of the
        other party in a `private` chat."""

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
    def __eq__(self, other: typing.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.message_id == other.message_id
            and self.chat_id == other.chat_id
        )

    @property
    def content_type(self) -> ContentType:
        """Type of content that the message contains."""

        for content in ContentType:
            if (
                content.value in self.__struct_fields__
                and getattr(self, content.value, Nothing) is not Nothing
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
        Full name, for `private` chat."""

        return (
            self.chat.full_name.unwrap()
            if self.chat.type == ChatType.PRIVATE
            else self.chat.title.unwrap()
        )


class _User(User):
    def __eq__(self, other: typing.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
        )

    @property
    def default_accent_color(self) -> DefaultAccentColor:
        """User's or bot's accent color (non-premium)."""

        return DefaultAccentColor(self.id % 7)

    @property
    def full_name(self) -> str:
        """User's or bot's full name (`first_name` + `last_name`)."""

        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class _Update(Update):
    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, self.__class__) and self.update_type == other.update_type

    @property
    def update_type(self) -> UpdateType:
        """Incoming update type."""

        return UpdateType(
            next(
                filter(
                    lambda x: bool(x[1]),
                    self.to_dict(exclude_fields={"update_id"}).items(),
                ),
            )[0],
        )


class _InputFile(typing.NamedTuple):
    filename: str
    """File name."""

    data: bytes
    """Bytes of file."""


class _InaccessibleMessage(InaccessibleMessage):
    date: typing.Literal[0]
    """Always 0. The field can be used to differentiate regular and inaccessible 
    messages."""


class _ReplyKeyboardMarkup(ReplyKeyboardMarkup):
    @property
    def empty_markup(self) -> "ReplyKeyboardRemove":
        """Empty keyboard to remove the custom keyboard."""

        return ReplyKeyboardRemove(remove_keyboard=True, selective=self.selective)
