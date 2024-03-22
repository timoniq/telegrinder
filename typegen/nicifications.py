"""
Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generated models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement methods/properties working only with model fields.
"""

import typing

from fntypes.option import Option, Some

from telegrinder.msgspec_utils import Nothing
from telegrinder.types import (
    Chat,
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


class _Chat(Chat):
    @property
    def full_name(self) -> Option[str]:
        """Optional. Full name (`first_name` + `last_name`) of the
        other party in a `private` chat."""

        return self.first_name.map(lambda x: x + " " + self.last_name.unwrap_or(""))


class _Message(Message):
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

    def __eq__(self, other: typing.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.message_id == other.message_id
            and self.chat_id == other.chat_id
        )


class _User(User):
    @property
    def default_accent_color(self) -> DefaultAccentColor:
        """User's or bot's accent color (non-premium)."""

        return DefaultAccentColor(self.id % 7)

    @property
    def full_name(self) -> str:
        """User's or bot's full name (`first_name` + `last_name`)."""

        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class _Update(Update):
    @property
    def update_type(self) -> Option[UpdateType]:
        """Incoming update type."""

        if update := next(
            filter(
                lambda x: bool(x[1]),
                self.to_dict(exclude_fields={"update_id"}).items(),
            ),
            None,
        ):
            return Some(UpdateType(update[0]))
        return Nothing


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
