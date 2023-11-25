import typing

import msgspec

from telegrinder.api.response import APIResponse
from telegrinder.client import ABCClient, AiohttpClient
from telegrinder.model import convert, decoder
from telegrinder.result import Error, Ok, Result
from telegrinder.types.methods import APIMethods

from .abc import ABCAPI, APIError, Token


def compose_data(client: ABCClient, data: dict) -> typing.Any:
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
        data = compose_data(self.http, data or {})
        response = await self.http.request_json(self.request_url + method, data=data)
        if response.get("ok"):
            assert "result" in response
            return Ok(response["result"])

        code, msg = response.get("error_code", 0), response.get("description")
        return Error(APIError(code, msg))

    async def request_raw(
        self,
        method: str,
        data: dict | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        data = compose_data(self.http, data or {})
        response_bytes = await self.http.request_bytes(
            self.request_url + method, data=data
        )
        response_skeleton: APIResponse = decoder.decode(
            response_bytes, type=APIResponse
        )
        return response_skeleton.to_result()
