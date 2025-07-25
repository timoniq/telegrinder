from __future__ import annotations

import asyncio
import pathlib
from functools import cached_property, wraps
from http import HTTPStatus

import msgspec
import typing_extensions as typing
from fntypes.library.misc import is_ok
from fntypes.library.monad.result import Error, Ok, Result

from telegrinder.api.error import APIError
from telegrinder.api.response import APIResponse
from telegrinder.api.token import Token
from telegrinder.client import ABCClient, AiohttpClient, MultipartFormProto
from telegrinder.client.aiohttp import DEFAULT_TIMEOUT
from telegrinder.model import decoder
from telegrinder.types.methods import APIMethods

type Json = str | int | float | bool | list[Json] | dict[str, Json] | None
type Data = dict[str, typing.Any]
type Files = dict[str, tuple[str, bytes]]
type APIRequestMethod[T: API, **P, R] = typing.Callable[
    typing.Concatenate[T, P],
    typing.Coroutine[typing.Any, typing.Any, Result[R, APIError]],
]

DEFAULT_MAX_RETRIES: typing.Final[int] = 5


def compose_data(
    client: ABCClient,
    data: Data,
    files: Files,
) -> MultipartFormProto:
    if not data and not files:
        return client.multipart_form_factory()
    return client.get_form(data=data, files=files)


def retryer[T: API, **P, R](func: APIRequestMethod[T, P, R], /) -> APIRequestMethod[T, P, R]:
    @wraps(func)
    async def wrapper(
        self: T,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[typing.Any, APIError]:
        retries_counter = 0

        while True:
            result = await func(self, *args, **kwargs)

            if is_ok(result) or not self.retryer_enabled or retries_counter >= self.max_retries:
                return result

            if result.error.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                await asyncio.sleep(result.error.retry_after.unwrap_or(5.0))

            elif result.error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR and "restart" in result.error.error:
                await asyncio.sleep(10.0)

            elif result.error.migrate_to_chat_id:
                kwargs["chat_id"] = result.error.migrate_to_chat_id.value

            retries_counter += 1

    return wrapper  # type: ignore


class API(APIMethods):
    """Bot API with available API methods and http client."""

    http: ABCClient

    API_URL = "https://api.telegram.org/"
    API_FILE_URL = "https://api.telegram.org/file/"

    def __init__(
        self,
        token: Token,
        *,
        http: ABCClient | None = None,
        enable_retryer: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.token = token
        self.http = http or AiohttpClient()
        self._retryer_enabled = enable_retryer
        self._max_retries = max_retries
        super().__init__(api=self)

    def __repr__(self) -> str:
        return "<{}: id={}, http={!r}, retryer_enabled={}, max_retries={}>".format(
            type(self).__name__,
            self.id,
            self.http,
            self._retryer_enabled,
            self._max_retries,
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

    @property
    def retryer_enabled(self) -> bool:
        return self._retryer_enabled

    @property
    def max_retries(self) -> int:
        return self._max_retries

    async def download_file(
        self,
        file_path: str | pathlib.Path,
        timeout: int | float = DEFAULT_TIMEOUT,
    ) -> bytes:
        return await self.http.request_content(
            url=f"{self.request_file_url}/{file_path}",
            timeout=timeout,
        )

    @retryer
    async def request(
        self,
        method: str,
        data: Data | None = None,
        files: Files | None = None,
        **kwargs: typing.Any,
    ) -> Result[Json, APIError]:
        """Request a `JSON` response using http method `POST` and passing data, files as `multipart/form-data`."""
        response = await self.http.request_json(
            url=self.request_url + method,
            method="POST",
            data=compose_data(self.http, data or {}, files or {}),
            **kwargs,
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
        **kwargs: typing.Any,
    ) -> Result[msgspec.Raw, APIError]:
        """Request a `raw` response using http method `POST` and passing data, files as `multipart/form-data`."""
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            method="POST",
            data=compose_data(self.http, data or {}, files or {}),
            **kwargs,
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API", "compose_data", "retryer")
