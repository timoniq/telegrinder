import pathlib
import typing
from abc import ABC, abstractmethod

import msgspec
from envparse import env
from fntypes.result import Result

from telegrinder.api.error import APIError
from telegrinder.client import ABCClient

from .error import InvalidTokenError


class Token(str):
    def __new__(cls, token: str) -> typing.Self:
        if token.count(":") != 1 or not token.split(":")[0].isdigit():
            raise InvalidTokenError("Invalid token, it should look like this '123:ABC'.")
        return super().__new__(cls, token)

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

    @property
    def bot_id(self) -> int:
        return int(self.split(":")[0])


class ABCAPI(ABC):
    http: ABCClient

    @abstractmethod
    async def request(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
    ) -> Result[list[typing.Any] | dict[str, typing.Any] | bool, APIError]:
        pass

    @abstractmethod
    async def request_raw(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        pass

    @property
    @abstractmethod
    def request_url(self) -> str:
        pass

    @property
    @abstractmethod
    def id(self) -> int:
        pass


__all__ = ("ABCAPI", "Token")
