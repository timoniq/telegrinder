import secrets
import typing
from functools import cached_property

import msgspec
from fntypes.result import Error, Ok, Result

from telegrinder.api.error import APIError
from telegrinder.api.response import APIResponse
from telegrinder.api.token import Token
from telegrinder.client import ABCClient, AiohttpClient
from telegrinder.model import decoder, is_none
from telegrinder.types.methods import APIMethods
from telegrinder.types.objects import InputFile


def compose_data(
    client: ABCClient,
    data: dict[str, typing.Any],
    files: dict[str, tuple[str, bytes]],
) -> typing.Any:
    if not data:
        return client.get_form(data=data, files=files)

    composed_data: dict[str, typing.Any] = {}
    stack = [(data, composed_data)]

    while stack:
        current_data, current_composed_data = stack.pop()

        for k, v in current_data.items():
            match v:
                case InputFile(filename, content):
                    attach_name = secrets.token_urlsafe(16)
                    files[attach_name] = (filename, content)
                    current_composed_data[k] = f"attach://{attach_name}"
                case msgspec.Struct() as struct:
                    new_composed_data = {}
                    current_composed_data[k] = new_composed_data
                    stack.append((msgspec.structs.asdict(struct), new_composed_data))
                case [msgspec.Struct(), *_] as seq:
                    current_composed_data[k] = []
                    for l in seq:
                        new_composed_data = {}
                        current_composed_data[k].append(new_composed_data)
                        stack.append((msgspec.structs.asdict(l), new_composed_data))
                case _ as value if not is_none(value):
                    current_composed_data[k] = value

    return client.get_form(data=composed_data, files=files)


class API(APIMethods):
    """Bot API with available API methods and http client."""

    API_URL = "https://api.telegram.org/"
    API_FILE_URL = "https://api.telegram.org/file/"

    token: Token
    http: ABCClient

    def __init__(self, token: Token, *, http: ABCClient | None = None) -> None:
        self.token = token
        self.http = http or AiohttpClient()
        super().__init__(self)

    def __repr__(self) -> str:
        return "<{}: token={!r}, http={!r}>".format(
            self.__class__.__name__,
            self.token,
            self.http,
        )

    @cached_property
    def id(self) -> int:
        return self.token.bot_id

    @property
    def request_url(self) -> str:
        return self.API_URL + f"bot{self.token}/"

    @property
    def request_file_url(self) -> str:
        return self.API_FILE_URL + f"bot{self.token}/"

    async def download_file(self, file_path: str) -> bytes:
        return await self.http.request_content(f"{self.request_file_url}/{file_path}")

    async def request(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> Result[dict[str, typing.Any] | list[typing.Any] | bool, APIError]:
        response = await self.http.request_json(
            url=self.request_url + method,
            data=compose_data(self.http, data or {}, files or {}),
        )
        if response.get("ok"):
            assert "result" in response
            return Ok(response["result"])
        return Error(
            APIError(
                code=response.get("error_code", 400),
                error=response.get("description"),
            )
        )

    async def request_raw(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            data=compose_data(self.http, data or {}, files or {}),
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API",)
