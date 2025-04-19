import pathlib
import typing
from functools import cached_property

from envparse import env

from .error import InvalidTokenError


class Token(str):
    def __new__(cls, token: str, /) -> typing.Self:
        if token.count(":") != 1 or not token.split(":")[0].isdigit():
            raise InvalidTokenError("Invalid token, it should look like this: 12345:ABCdef")
        return super().__new__(cls, token)

    def __repr__(self) -> str:
        return f"<Token: {self.bot_id}:{self.split(':')[1][:6]}...>"

    @classmethod
    def from_env(
        cls,
        var_name: str = "BOT_TOKEN",
        *,
        is_read: bool = False,
        path_to_envfile: str | pathlib.Path | None = None,
    ) -> typing.Self:
        if not is_read:
            env.read_envfile(path_to_envfile)
        return cls(env.str(var_name))

    @cached_property
    def bot_id(self) -> int:
        return int(self.split(":")[0])


__all__ = ("Token",)
