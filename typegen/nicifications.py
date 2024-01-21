"""
Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generated models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement methods/properties working only with model fields.
"""
from telegrinder.model import Model
from telegrinder.types import Message, User


class _Message(Message):
    @property
    def from_user(self) -> "User":
        """`from_user` instead of `from_.unwrap()`"""

        return self.from_.unwrap()

    def __eq__(self, other: "Message"):
        return self.message_id == other.message_id and self.chat.id == other.chat.id


class _User(User):
    @property
    def full_name(self) -> str:
        """User's or bot's `first_name` + `last_name`."""

        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class _InputFile(Model):
    filename: str
    """Filename."""

    data: bytes
    """Bytes of file."""
