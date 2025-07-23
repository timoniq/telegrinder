from __future__ import annotations

import asyncio
import ssl as ssllib
import typing

import aiohttp
import aiohttp.hdrs
import aiohttp.http
import certifi
from aiohttp import ClientSession, TCPConnector

from telegrinder.__meta__ import __version__
from telegrinder.client.abc import ABCClient
from telegrinder.msgspec_utils import json

if typing.TYPE_CHECKING:
    from aiohttp import BaseConnector, ClientResponse

type Data = dict[str, typing.Any] | aiohttp.formdata.FormData
type Response = ClientResponse
type Timeout = int | float | aiohttp.ClientTimeout

DEFAULT_TIMEOUT: typing.Final[float] = 30.0
DEFAULT_LIMIT_SIMULTANEOUS_CONNECTIONS: typing.Final[int] = 100
DEFAULT_TTL_DNS_CACHE: typing.Final[int] = 3600
DEFAULT_HEADERS: typing.Final[dict[str, str]] = {
    aiohttp.hdrs.USER_AGENT: f"{aiohttp.http.SERVER_SOFTWARE} telegrinder/{__version__}"
}


def get_client_timeout(total_timeout: Timeout, /) -> aiohttp.ClientTimeout:
    return (
        total_timeout
        if isinstance(total_timeout, aiohttp.ClientTimeout)
        else aiohttp.ClientTimeout(total=float(total_timeout))
    )


class AiohttpClient(ABCClient):
    """HTTP client based on `aiohttp` module."""

    session_params: dict[str, typing.Any]

    CONNECTION_TIMEOUT_ERRORS = (aiohttp.client.ServerConnectionError,)
    CLIENT_CONNECTION_ERRORS = (
        aiohttp.client.ClientConnectionError,
        aiohttp.client.ClientConnectorError,
        aiohttp.ClientOSError,
    )

    __slots__ = (
        "_session",
        "limit",
        "ttl_dns_cache",
        "session_params",
        "ssl",
        "_connector",
        "verify_ssl",
        "limit",
        "ttl_dns_cache",
        "_timeout",
    )

    def __init__(
        self,
        session: ClientSession | None = None,
        connector: BaseConnector | None = None,
        ssl: ssllib.SSLContext | None = None,
        verify_ssl: bool = True,
        timeout: Timeout = DEFAULT_TIMEOUT,
        limit: int = DEFAULT_LIMIT_SIMULTANEOUS_CONNECTIONS,
        ttl_dns_cache: int = DEFAULT_TTL_DNS_CACHE,
        **session_params: typing.Any,
    ) -> None:
        self.ssl = ssl or ssllib.create_default_context(cafile=certifi.where())
        self.limit = limit
        self.ttl_dns_cache = ttl_dns_cache
        self.verify_ssl = verify_ssl
        self.session_params = dict(headers=DEFAULT_HEADERS) | session_params
        self._session = session
        self._connector = connector or None
        self._timeout = get_client_timeout(timeout)

    def __repr__(self) -> str:
        return "<{}: session={!r}, timeout={}, closed={}>".format(
            type(self).__name__,
            self._session,
            self._timeout,
            True if self._session is None else self._session.closed,
        )

    def __del__(self) -> None:
        if self._session and not self._session.closed:
            if self._session._connector is not None and self._session._connector_owner:
                self._session._connector._close()
            self._session._connector = None

    @classmethod
    def multipart_form_factory(cls) -> aiohttp.formdata.FormData:
        return aiohttp.formdata.FormData(quote_fields=False)

    @property
    def timeout(self) -> float:
        return float(self._timeout.total or 0.0)

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        *,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> Response:
        if not self._session:
            self._session = ClientSession(
                connector=self._connector
                or TCPConnector(
                    ssl=self.ssl,
                    verify_ssl=self.verify_ssl,
                    limit=self.limit,
                    ttl_dns_cache=self.ttl_dns_cache,
                ),
                json_serialize=json.dumps,
                **self.session_params,
            )

        async with self._session.request(
            method=method,
            url=url,
            data=data,
            timeout=self._timeout if timeout is None else get_client_timeout(timeout),
            **kwargs,
        ) as response:
            await response.read()
            return response

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        *,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        response = await self.request_raw(url, method, data, timeout=timeout, **kwargs)
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
        *,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> str:
        response = await self.request_raw(url, method, data, timeout=timeout, **kwargs)
        return await response.text(encoding="UTF-8")

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        *,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, timeout=timeout, **kwargs)
        if response._body is None:
            await response.read()
        return response._body or bytes()

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        *,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, timeout=timeout, **kwargs)
        return response._body or bytes()

    async def close(self, *, gracefully: bool = False) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

        if gracefully:
            # Wait 250 ms for graceful shutdown SSL connections
            await asyncio.sleep(0.250)


__all__ = ("AiohttpClient",)
