from abc import ABC, abstractmethod
import typing

import msgspec

from telegrinder.client import ABCClient
from telegrinder.result import Result
from telegrinder.api.error import APIError

from envparse import env


class Token(str):
    @classmethod
    def from_env(cls, var_name: str = "BOT_TOKEN", is_read: bool = False) -> "Token":
        if not is_read:
            env.read_envfile()
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
        data: dict | None = None,
    ) -> Result[list | dict | bool, APIError]:
        pass

    @abstractmethod
    async def request_raw(
        self,
        method: str,
        data: dict | None = None,
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
