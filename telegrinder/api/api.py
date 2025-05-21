from __future__ import annotations

import asyncio
from functools import cached_property, wraps
from http import HTTPStatus

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
type Data = dict[str, typing.Any]
type Files = dict[str, tuple[str, bytes]]
type APIMethod[T: API[typing.Any], **P, R] = typing.Callable[
    typing.Concatenate[T, P],
    typing.Coroutine[typing.Any, typing.Any, Result[R, APIError]],
]

HTTPClient = typing.TypeVar("HTTPClient", bound=ABCClient, default=AiohttpClient)


def compose_data[MultipartForm: MultipartFormProto](
    client: ABCClient[MultipartForm],
    data: Data,
    files: Files,
) -> MultipartForm:
    if not data and not files:
        return client.multipart_form_factory()
    return client.get_form(data=data, files=files)


def retryer[T: API[typing.Any], **P, R](func: APIMethod[T, P, R], /) -> APIMethod[T, P, R]:
    @wraps(func)
    async def wrapper(
        self: T,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[typing.Any, APIError]:
        while True:
            match await func(self, *args, **kwargs):
                case Error(error) if error.status_code == HTTPStatus.TOO_MANY_REQUESTS and self.retryer_enabled:
                    await asyncio.sleep(error.retry_after.unwrap())
                case _ as response:
                    return response

    return wrapper  # type: ignore


class API(APIMethods[HTTPClient], typing.Generic[HTTPClient]):
    """Bot API with available API methods and http client."""

    http: HTTPClient

    API_URL = "https://api.telegram.org/"
    API_FILE_URL = "https://api.telegram.org/file/"

    def __init__(
        self,
        token: Token,
        *,
        http: HTTPClient | None = None,
        enable_retryer: bool = True,
    ) -> None:
        self.token = token
        self.http = http or AiohttpClient()  # type: ignore
        self.retryer_enabled = enable_retryer
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

    @retryer
    async def request(
        self,
        method: str,
        data: Data | None = None,
        files: Files | None = None,
    ) -> Result[Json, APIError]:
        """Request a `JSON` response using http method `POST`and passing data, files as `multipart/form-data`."""
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
                data=response.get("parameters", {}),
            ),
        )

    @retryer
    async def request_raw(
        self,
        method: str,
        data: Data | None = None,
        files: Files | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        """Request a `raw` response using http method `POST` and passing data, files as `multipart/form-data`."""
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            method="POST",
            data=compose_data(self.http, data or {}, files or {}),
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API", "compose_data", "retryer")
