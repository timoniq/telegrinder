from abc import ABC, abstractmethod
import typing
from telegrinder.http import ABCClient
from telegrinder.tools import Result

Token = typing.NewType("Token", str)


class APIError(BaseException):
    def __init__(self, code: int, error: typing.Optional[str] = None):
        self.code, self.error = code, error


class ABCAPI(ABC):
    http: ABCClient

    @abstractmethod
    async def request(
        self,
        method: str,
        data: typing.Optional[dict] = None,
    ) -> Result[typing.Union[list, dict], APIError]:
        pass
