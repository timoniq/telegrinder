import msgspec

from .abc import ABCAPI, APIError, Token
import typing
from telegrinder.result import Result
from telegrinder.client import ABCClient, AiohttpClient
from telegrinder.types.methods import APIMethods
from telegrinder.model import convert
from telegrinder.api.response import APIResponse


def compose_data(client: ABCClient, data: dict) -> typing.Any:
    data = {k: convert(v) for k, v in data.items()}
    if any(isinstance(v, tuple) for v in data.values()):
        data = client.get_form(data)
    return data


class API(ABCAPI, APIMethods):
    API_URL = "https://api.telegram.org/"

    def __init__(self, token: Token, http: ABCClient | None = None):
        self.token = token
        self.http = http or AiohttpClient()
        super().__init__(self)

    @property
    def id(self) -> int:
        return int(self.token.split(":")[0])

    @property
    def request_url(self) -> str:
        return self.API_URL + f"bot{self.token}/"

    async def request(
        self,
        method: str,
        data: dict | None = None,
    ) -> Result[dict | list | bool, APIError]:
        data = compose_data(self.http, data)
        response = await self.http.request_json(self.request_url + method, data=data)
        if response.get("ok"):
            assert "result" in response
            return Result(True, value=response["result"])

        code, msg = response.get("error_code"), response.get("description")
        return Result(False, error=APIError(code, msg))

    async def request_raw(
        self,
        method: str,
        data: dict | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        data = compose_data(self.http, data)
        response_bytes = await self.http.request_bytes(
            self.request_url + method, data=data
        )
        response_skeleton: APIResponse = msgspec.json.decode(
            response_bytes, type=APIResponse
        )
        return response_skeleton.to_result()
