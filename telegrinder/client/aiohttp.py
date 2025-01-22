import ssl
import typing

import aiohttp
import certifi
from aiohttp import ClientSession, TCPConnector

import telegrinder.msgspec_json as json
from telegrinder.client.abc import ABCClient

if typing.TYPE_CHECKING:
    from aiohttp import ClientResponse

type Data = dict[str, typing.Any] | aiohttp.formdata.FormData
type Response = ClientResponse


class AiohttpClient(ABCClient[aiohttp.formdata.FormData]):
    """HTTP client based on `aiohttp` module."""

    CONNECTION_TIMEOUT_ERRORS = (
        aiohttp.client.ServerConnectionError,
        TimeoutError,
    )
    CLIENT_CONNECTION_ERRORS = (
        aiohttp.client.ClientConnectionError,
        aiohttp.client.ClientConnectorError,
        aiohttp.ClientOSError,
    )

    def __init__(
        self,
        session: ClientSession | None = None,
        timeout: aiohttp.ClientTimeout | None = None,
        **session_params: typing.Any,
    ) -> None:
        self.session = session
        self.session_params = session_params
        self.timeout = timeout or aiohttp.ClientTimeout(total=0)

    def __repr__(self) -> str:
        return "<{}: session={!r}, timeout={}, closed={}>".format(
            self.__class__.__name__,
            self.session,
            self.timeout,
            True if self.session is None else self.session.closed,
        )

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> Response:
        if not self.session:
            self.session = ClientSession(
                connector=TCPConnector(ssl=ssl.create_default_context(cafile=certifi.where())),
                json_serialize=json.dumps,
                **self.session_params,
            )

        async with self.session.request(
            url=url,
            method=method,
            data=data,
            timeout=self.timeout,
            **kwargs,
        ) as response:
            await response.read()
            return response

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="UTF-8",
            loads=json.loads,
            content_type=None,
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)  # type: ignore
        return await response.text(encoding="UTF-8")

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)  # type: ignore
        if response._body is None:
            await response.read()
        return response._body or bytes()

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body or bytes()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    @classmethod
    def multipart_form_factory(cls) -> aiohttp.formdata.FormData:
        return aiohttp.formdata.FormData(quote_fields=False)

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector._close()
            self.session._connector = None


__all__ = ("AiohttpClient",)
