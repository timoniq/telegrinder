from .abc import ABCAPI, APIError, Token
import typing
from telegrinder.tools import Result
from telegrinder.http import ABCClient, AiohttpClient


class API(ABCAPI):
    API_URL = "https://api.telegram.org/"

    def __init__(self, token: Token, http: typing.Optional[ABCClient] = None):
        self.token = token
        self._request_url = self.API_URL + f"bot{self.token}/"
        self.http = http or AiohttpClient()

    async def request(
        self,
        method: str,
        data: typing.Optional[dict] = None,
    ) -> Result[typing.Union[dict, list], APIError]:
        response = await self.http.request_json(self._request_url + method, json=data)
        if response.get("ok"):
            assert "result" in response
            return Result(True, value=response["result"])

        code, msg = response.get("error_code"), response.get("error_description")
        return Result(False, error=APIError(code, msg))
