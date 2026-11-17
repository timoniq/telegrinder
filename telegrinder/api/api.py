import pathlib
import typing
from datetime import timedelta
from functools import cached_property

import msgspec
from kungfu.library.monad.result import Error, Ok, Result
from msgspex import decoder

from telegrinder.api.error import APIError
from telegrinder.api.response import APIResponse
from telegrinder.api.retryer import APIRetryer, retryer
from telegrinder.api.token import Token
from telegrinder.client import ABCClient, WreqClient
from telegrinder.tools.fullname import fullname
from telegrinder.types.methods import APIMethods, APIResult

type JSON = str | int | float | bool | list[JSON] | dict[str, JSON] | None
type Data = dict[str, typing.Any]
type Files = dict[str, tuple[str, bytes]]
type APIRequestMethod[T: API, **P, R] = typing.Callable[
    typing.Concatenate[T, P],
    typing.Coroutine[typing.Any, typing.Any, Result[R, APIError]],
]

DEFAULT_MAX_RETRIES: typing.Final = 5
DEFAULT_TIMEOUT: typing.Final = timedelta(seconds=30)


class API(APIMethods):
    API_URL = "https://api.telegram.org/"
    API_FILE_URL = "https://api.telegram.org/file/"

    @typing.overload
    def __init__(self, token: Token) -> None: ...

    @typing.overload
    def __init__(self, token: Token, *, http: ABCClient) -> None: ...

    @typing.overload
    def __init__(
        self,
        token: Token,
        *,
        retryer: typing.Literal[True] = True,
        http: ABCClient = ...,
        max_retries: int = ...,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        token: Token,
        *,
        retryer: typing.Literal[False],
        http: ABCClient = ...,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        token: Token,
        *,
        retryer: APIRetryer,
        http: ABCClient = ...,
    ) -> None: ...

    def __init__(
        self,
        token: Token,
        *,
        http: ABCClient | None = None,
        retryer: bool | APIRetryer = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.token = token
        self.http: ABCClient = http or WreqClient()
        self.retryer = APIRetryer(retries=max_retries) if retryer is True else None if retryer is False else retryer
        self._retryer_is_enabled = True if isinstance(retryer, APIRetryer) else retryer
        self._max_retries = self.retryer.retries if self.retryer is not None else max_retries

        super().__init__(api=self)

    def __repr__(self) -> str:
        return "<{}: id={}, http={!r}, retryer={!r}>".format(
            fullname(self),
            self.id,
            self.http,
            self.retryer,
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
    def retryer_is_enabled(self) -> bool:
        return self._retryer_is_enabled

    @property
    def max_retries(self) -> int:
        return self._max_retries

    @retryer
    async def download_file(
        self,
        file_path: str | pathlib.Path,
        timeout: int | float | timedelta = DEFAULT_TIMEOUT,
    ) -> APIResult[bytes]:
        response = await self.http.request(
            url=f"{self.request_file_url}/{file_path}",
            timeout=timeout,
        )

        if response.status.is_success:
            return Ok(response.content)

        error = decoder.decode(response.content, type=APIResponse)
        return Error(
            APIError(
                code=error.error_code,
                error=error.description,
                data=error.parameters,
                is_download_file=True,
            ),
        )

    @retryer
    async def request(
        self,
        method: str,
        data: Data | None = None,
        files: Files | None = None,
        **kwargs: typing.Any,
    ) -> APIResult[JSON]:
        """Request a `JSON` response using http method `POST` and passing data & files as `multipart`."""
        response = await self.http.request_json(
            url=self.request_url + method,
            method="POST",
            data=self.http.get_form(data=data, files=files),
            **kwargs,
        )

        if response.get("ok", False) is True:
            return Ok(response.get("result"))

        return Error(
            APIError(
                code=response.get("error_code", 400),
                error=response.get("description", "Something went wrong"),
                data=response.get("parameters", {}),
                method=method,
            ),
        )

    @retryer
    async def request_raw(
        self,
        method: str,
        data: Data | None = None,
        files: Files | None = None,
        **kwargs: typing.Any,
    ) -> APIResult[msgspec.Raw]:
        """Request a `raw` response using http method `POST` and passing data & files as `multipart`."""
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            method="POST",
            data=self.http.get_form(data=data, files=files),
            **kwargs,
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result(method)


__all__ = ("API",)
