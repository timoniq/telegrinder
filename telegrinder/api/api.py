from .abc import ABCAPI, APIError, Token
import typing
from telegrinder.tools import Result
from telegrinder.http import ABCClient, AiohttpClient
from telegrinder.types.methods import APIMethods
from telegrinder.types.objects import BaseModel
from telegrinder.modules import json, logger


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
        data = {
            k: (v if not isinstance(v, BaseModel) else v.get_dict())
            for k, v in data.items()
            if v is not None
        }
        logger.info("Making API request {}: {}".format(method, data))
        response = await self.http.request_json(self._request_url + method, json=data)
        logger.info("Got response: {}".format(response))
        if response.get("ok"):
            assert "result" in response
            return Result(True, value=alias(response["result"]))

        code, msg = response.get("error_code"), response.get("description")
        return Result(False, error=APIError(code, msg))
