"""
Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generated models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement methods/properties working only with model fields.
"""

import typing

from telegrinder.model import Model
from telegrinder.msgspec_utils import Nothing
from telegrinder.types import ContentType, Message, User


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
        """`from_user` instead of `from_.unwrap()`"""

        return self.from_.unwrap()

    def __eq__(self, other: "Message") -> bool:
        return self.message_id == other.message_id and self.chat.id == other.chat.id


class _User(User):
    @property
    def full_name(self) -> str:
        """User's or bot's `first_name` + `last_name`."""

        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class _InputFile(typing.NamedTuple):
    filename: str
    """Filename."""

    data: bytes
    """Bytes of file."""


class _InaccessibleMessage(Model):
    date: typing.Literal[0]
    """Always 0. The field can be used to differentiate regular and inaccessible 
    messages."""
