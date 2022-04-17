from abc import ABC, abstractmethod
import typing
from telegrinder.http import ABCClient
from telegrinder.tools import Result
from telegrinder.api.error import APIError

Token = typing.NewType("Token", str)


class ABCAPI(ABC):
    http: ABCClient

    @abstractmethod
    async def request(
        self,
        method: str,
        data: typing.Optional[dict] = None,
    ) -> Result[typing.Union[list, dict, bool], APIError]:
        pass
