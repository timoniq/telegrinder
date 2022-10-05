import msgspec

from .abc import ABCAPI, APIError, Token
import typing
from telegrinder.tools import Result
from telegrinder.client import ABCClient, AiohttpClient
from telegrinder.types.methods import APIMethods
from telegrinder.model import convert
from telegrinder.api.response import APIResponse
from telegrinder.modules import logger


def alias(d: typing.Any) -> typing.Any:
    if not isinstance(d, dict):
        if isinstance(d, list):
            return [alias(e) for e in d]
        return d
    for (k, v) in d.copy().items():
        if k in ("from",):
            d[k + "_"] = alias(d.pop(k))
        else:
            d[k] = alias(d[k])
    return d


class API(ABCAPI, APIMethods):
    API_URL = "https://api.telegram.org/"

    def __init__(self, token: Token, http: typing.Optional[ABCClient] = None):
        self.token = token
        self._request_url = self.API_URL + f"bot{self.token}/"
        self.http = http or AiohttpClient()
        super().__init__(self)

    async def request(
        self,
        method: str,
        data: typing.Optional[dict] = None,
    ) -> Result[typing.Union[dict, list, bool], APIError]:
        data = convert(data)
        logger.debug("Making API request {}: {}".format(method, data))
        response = await self.http.request_json(self._request_url + method, json=data)
        logger.debug("Got response: {}".format(response))
        if response.get("ok"):
            assert "result" in response
            return Result(True, value=alias(response["result"]))

        code, msg = response.get("error_code"), response.get("description")
        return Result(False, error=APIError(code, msg))

    async def request_raw(
        self, method: str, data: typing.Optional[dict] = None
    ) -> Result[msgspec.Raw, APIError]:
        data = convert(data)
        response_bytes = await self.http.request_bytes(
            self._request_url + method, json=data
        )
        response_skeleton: APIResponse = msgspec.json.decode(
            response_bytes, type=APIResponse
        )
        return response_skeleton.to_result()
