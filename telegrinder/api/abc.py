from abc import ABC, abstractmethod
import typing
from telegrinder.http_ import ABCClient
from telegrinder.tools import Result
from telegrinder.api.error import APIError

from envparse import env


class Token(str):
    @classmethod
    def from_env(cls, var_name: str = "BOT_TOKEN", is_read: bool = False) -> "Token":
        if not is_read:
            env.read_envfile()
        return cls(env.str(var_name))


class ABCAPI(ABC):
    http: ABCClient

    @abstractmethod
    async def request(
        self,
        method: str,
        data: typing.Optional[dict] = None,
    ) -> Result[typing.Union[list, dict, bool], APIError]:
        pass
