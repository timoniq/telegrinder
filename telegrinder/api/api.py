import typing

import msgspec
from fntypes.result import Error, Ok, Result

from telegrinder.api.response import APIResponse
from telegrinder.client import ABCClient, AiohttpClient
from telegrinder.model import convert, decoder
from telegrinder.types.methods import APIMethods

from .abc import ABCAPI, APIError, Token


def compose_data(client: ABCClient, data: dict[str, typing.Any]) -> typing.Any:
    data = {k: convert(v) for k, v in data.items()}
    if any(isinstance(v, tuple) for v in data.values()):
        data = client.get_form(data)
    return data


class API(ABCAPI, APIMethods):
    API_URL: typing.ClassVar[str] = "https://api.telegram.org/"

    def __init__(self, token: Token, *, http: ABCClient | None = None):
        self.token = token
        self.http = http or AiohttpClient()
        super().__init__(self)

    @property
    def id(self) -> int:
        return self.token.bot_id

    @property
    def request_url(self) -> str:
        return self.API_URL + f"bot{self.token}/"

    async def request(
        self,
        method: str,
        data: dict | None = None,
    ) -> Result[dict | list | bool, APIError]:
        response = await self.http.request_json(
            url=self.request_url + method,
            data=compose_data(self.http, data or {})
        )
        if response.get("ok"):
            assert "result" in response
            return Ok(response["result"])
        return Error(APIError(
            code=response.get("error_code", 0),
            error=response.get("description"),
        ))

    async def request_raw(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            data=compose_data(self.http, data or {}),
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API",)
