from .abc import ABCAPI, APIError, Token
import typing
from telegrinder.tools import Result
from telegrinder.http import ABCClient, AiohttpClient
from telegrinder.types.methods import APIMethods
from pydantic import BaseModel


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
            k: v if not isinstance(v, BaseModel) else v.dict()
            for k, v in data.items()
            if v is not None
        }
        response = await self.http.request_json(self._request_url + method, json=data)
        if response.get("ok"):
            assert "result" in response
            return Result(True, value=response["result"])

        code, msg = response.get("error_code"), response.get("error_description")
        return Result(False, error=APIError(code, msg))
