from functools import cached_property

import msgspec
import typing_extensions as typing
from fntypes.result import Error, Ok, Result

from telegrinder.api.error import APIError
from telegrinder.api.response import APIResponse
from telegrinder.api.token import Token
from telegrinder.client import ABCClient, AiohttpClient, MultipartFormProto
from telegrinder.model import decoder
from telegrinder.types.methods import APIMethods

type Json = str | int | float | bool | list[Json] | dict[str, Json] | None

HTTPClient = typing.TypeVar("HTTPClient", bound=ABCClient, default=AiohttpClient)


def compose_data[MultipartForm: MultipartFormProto](
    client: ABCClient[MultipartForm],
    data: dict[str, typing.Any],
    files: dict[str, tuple[str, bytes]],
) -> MultipartForm:
    if not data and not files:
        return client.multipart_form_factory()
    return client.get_form(data=data, files=files)


class API(APIMethods[HTTPClient], typing.Generic[HTTPClient]):
    """Bot API with available API methods and http client."""

    API_URL = "https://api.telegram.org/"
    API_FILE_URL = "https://api.telegram.org/file/"

    token: Token
    http: HTTPClient

    def __init__(self, token: Token, *, http: HTTPClient | None = None) -> None:
        self.token = token
        self.http = http or AiohttpClient()  # type: ignore
        super().__init__(api=self)

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
    ) -> Result[Json, APIError]:
        """Request a `JSON` response with the `POST` HTTP method and passing data, files as `multipart/form-data`."""
        response = await self.http.request_json(
            url=self.request_url + method,
            method="POST",
            data=compose_data(self.http, data or {}, files or {}),
        )
        if response.get("ok", False) is True:
            return Ok(response["result"])
        return Error(
            APIError(
                code=response.get("error_code", 400),
                error=response.get("description", "Something went wrong"),
            ),
        )

    async def request_raw(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        """Request a `raw` response with the `POST` HTTP method and passing data, files as `multipart/form-data`."""
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            method="POST",
            data=compose_data(self.http, data or {}, files or {}),
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API",)
