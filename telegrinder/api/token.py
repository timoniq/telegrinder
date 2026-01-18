import typing
from functools import cached_property

from telegrinder.api.error import InvalidTokenError
from telegrinder.env import take


class Token(str):
    def __new__(cls, token: str, /) -> typing.Self:
        if token.count(":") != 1 or not token.split(":")[0].isdigit():
            raise InvalidTokenError("Invalid token format, it should look like 12345:ABCdef")
        return super().__new__(cls, token)

    def __repr__(self) -> str:
        return f"<Token: {self.bot_id}:{self.token[:9]}...>"

    @classmethod
    def from_env(cls, var_name: str = "BOT_TOKEN") -> typing.Self:
        return cls(take(var_name))

    @cached_property
    def token(self) -> str:
        return self.split(":")[1]

    @cached_property
    def bot_id(self) -> int:
        return int(self.split(":")[0])


__all__ = ("Token",)
