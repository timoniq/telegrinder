from __future__ import annotations

import io
import ssl
import typing

import certifi

from telegrinder.client.abc import ABCClient
from telegrinder.msgspec_utils import json

if typing.TYPE_CHECKING:
    from aiosonic import (  # type: ignore
        Connection,
        HTTPClient,
        HttpResponse,
        MultipartForm,
        Proxy,
        TCPConnector,
        Timeouts,
    )

type Data = dict[str, typing.Any] | MultipartForm
type Response = HttpResponse

AIOSONIC_OBJECTS = (
    "Connection",
    "HTTPClient",
    "HttpResponse",
    "Proxy",
    "TCPConnector",
    "Timeouts",
)


def init_aiosonic_module(client_class: type[ABCClient[typing.Any]], /) -> None:
    try:
        import aiosonic  # type: ignore
        import aiosonic.exceptions  # type: ignore
    except ImportError:
        raise ImportError(
            "Module 'aiosonic' is not installed. You can install as follows: pip install aiosonic"
        ) from None

    globalns = globals()
    for name in AIOSONIC_OBJECTS:
        globalns.setdefault(name, getattr(aiosonic, name))

    if "MultipartForm" not in globalns:
        globalns["MultipartForm"] = type("MultiPartForm", (_MultipartForm, aiosonic.MultipartForm), {})

    if not client_class.CONNECTION_TIMEOUT_ERRORS:
        client_class.CONNECTION_TIMEOUT_ERRORS = (
            aiosonic.exceptions.ConnectTimeout,
            aiosonic.exceptions.RequestTimeout,
            TimeoutError,
        )

    if not client_class.CLIENT_CONNECTION_ERRORS:
        client_class.CLIENT_CONNECTION_ERRORS = (
            aiosonic.exceptions.ConnectionDisconnected,
            aiosonic.exceptions.ConnectionPoolAcquireTimeout,
        )


class _MultipartForm(MultipartForm if typing.TYPE_CHECKING else object):
    async def _generate_chunks(self) -> typing.AsyncGenerator[bytes, None]:
        for field in self.fields:
            yield (f"--{self.boundary}\r\n").encode()

            if isinstance(field[1], io.IOBase):
                yield (
                    "Content-Type: application/octet-stream\r\n"
                    "Content-Disposition: form-data; " + f'name="{field[0]}"; filename="{field[2]}"\r\n\r\n'
                ).encode()

                async for data in self._read_file(field[1]):
                    yield data + b"\r\n"

                field[1].close()
            else:
                yield (
                    "Content-Type: text/plain; charset=utf-8\r\n"
                    f'Content-Disposition: form-data; name="{field[0]}"\r\n\r\n'
                ).encode()
                yield field[1].encode() + b"\r\n"

        yield (f"--{self.boundary}--").encode()

    async def get_body_size(self) -> tuple[bytes, int]:
        if not self.fields:
            return b"", 0
        return await super().get_body_size()

    def get_headers(self, size: int | None = None) -> dict[str, str]:
        if not self.fields:
            return {"Content-Type": "application/x-www-form-urlencoded"}
        return super().get_headers(size)


class AiosonicClient(ABCClient["MultipartForm"]):
    """HTTP client based on `aiosonic` module."""

    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        init_aiosonic_module(cls)
        return super().__init_subclass__(*args, **kwargs)

    def __init__(
        self,
        *,
        verify_ssl: bool = True,
        tpc_pool_size: int = 25,
        tpc_timeouts: Timeouts | None = None,
        proxy: Proxy | None = None,
        conn_max_requests: int = 100,
        use_dns_cache: bool = True,
        handle_cookies: bool = False,
        ttl_dns_cache: int = 10000,
        **kwargs: typing.Any,
    ) -> None:
        init_aiosonic_module(self.__class__)
        self.ssl = ssl.create_default_context(cafile=certifi.where())
        self.proxy = proxy
        self.verify_ssl = verify_ssl
        self.handle_cookies = handle_cookies
        self.tpc_timeouts = tpc_timeouts or Timeouts()
        self.tcp_connector = TCPConnector(
            pool_size=tpc_pool_size,
            timeouts=self.tpc_timeouts,
            connection_cls=Connection,
            conn_max_requests=conn_max_requests,
            use_dns_cache=use_dns_cache,
            ttl_dns_cache=ttl_dns_cache,
            **kwargs,
        )
        self.client: HTTPClient | None = None

    def __repr__(self) -> str:
        return "<{}: proxy={!r}, tpc_timeouts={!r}, tcp_connector={!r}, client={!r}>".format(
            self.__class__.__name__,
            self.proxy,
            self.tpc_timeouts,
            self.tcp_connector,
            self.client,
        )

    @classmethod
    def multipart_form_factory(cls) -> MultipartForm:
        return MultipartForm()

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> Response:
        if self.client is None:
            self.client = HTTPClient(
                connector=self.tcp_connector,
                handle_cookies=self.handle_cookies,
                verify_ssl=self.verify_ssl,
                proxy=self.proxy,
            )

        return await self.client.request(  # type: ignore
            url=url,
            method=method,
            data=data,
            json_serializer=json.dumps,
            ssl=self.ssl,
            **kwargs,
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text()

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        return json.loads(await self.request_content(url, method, data, **kwargs))

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response.body

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.content()

    async def close(self) -> None:
        if self.client is not None:
            await self.client.connector.cleanup()
            self.client = None


__all__ = ("AiosonicClient",)
