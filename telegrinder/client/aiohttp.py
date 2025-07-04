from __future__ import annotations

import asyncio
import ssl
import typing

import aiohttp
import certifi
from aiohttp import BasicAuth, ClientSession, TCPConnector
from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE

from telegrinder.__meta__ import __version__
from telegrinder.client.abc import ABCClient
from telegrinder.msgspec_utils import json

if typing.TYPE_CHECKING:
    from aiohttp import ClientResponse

type Data = dict[str, typing.Any] | aiohttp.formdata.FormData
type Response = ClientResponse
type Timeout = int | float | aiohttp.ClientTimeout
type Proxy = str | tuple[str, BasicAuth]
type ProxyChain = typing.Iterable[Proxy]
type ProxyType = Proxy | ProxyChain

DEFAULT_TIMEOUT: typing.Final[float] = 30.0
DEFAULT_LIMIT_SIMULTANEOUS_CONNECTIONS: typing.Final[int] = 100
DEFAULT_TTL_DNS_CACHE: typing.Final[int] = 3600
DEFAULT_HEADERS: typing.Final[dict[str, str]] = {USER_AGENT: f"{SERVER_SOFTWARE} telegrinder/{__version__}"}


def _get_client_timeout(timeout: Timeout, /) -> aiohttp.ClientTimeout:
    return timeout if isinstance(timeout, aiohttp.ClientTimeout) else aiohttp.ClientTimeout(total=float(timeout))


def _prepare_proxy_connector(
    proxy: ProxyType,
    /,
) -> tuple[type[TCPConnector], dict[str, typing.Any] | list[typing.Any]]:
    try:
        from aiohttp_socks import ChainProxyConnector, ProxyConnector, ProxyInfo  # type: ignore
        from aiohttp_socks.utils import parse_proxy_url  # type: ignore
    except ImportError:
        raise ImportError(
            "Module `aiohttp-socks` is not installed. You can install as follows: pip install aiohttp-socks "
            'or pip install "telegrinder[socks]"',
        ) from None

    match proxy:
        case str() | (str(), BasicAuth()):
            proxy_chain = (proxy,)
        case _:
            proxy_chain = proxy

    proxy_infos = list()  # type: ignore

    for _proxy in proxy_chain:
        url, basic = (_proxy, None) if isinstance(_proxy, str) else _proxy
        proxy_type, host, port, username, password = parse_proxy_url(url)  # type: ignore

        if basic is not None:
            username, password = basic.login, basic.password  # type: ignore

        proxy_infos.append(
            ProxyInfo(  # type: ignore
                proxy_type,
                host,
                port,
                username,
                password,
                rdns=True,
            ),
        )

    return (
        (
            ProxyConnector,  # type: ignore
            proxy_infos[0]._asdict(),  # type: ignore
        )
        if len(proxy_infos) == 1
        else (ChainProxyConnector, proxy_infos)
    )  # type: ignore


class AiohttpClient(ABCClient):
    """HTTP client based on `aiohttp` module."""

    CONNECTION_TIMEOUT_ERRORS = (aiohttp.client.ServerConnectionError,)
    CLIENT_CONNECTION_ERRORS = (
        aiohttp.client.ClientConnectionError,
        aiohttp.client.ClientConnectorError,
        aiohttp.ClientOSError,
    )

    __slots__ = (
        "session",
        "limit",
        "ttl_dns_cache",
        "session_params",
        "_proxy",
        "_tcp_connector_kwargs",
        "_tcp_connector_class",
    )

    def __init__(
        self,
        session: ClientSession | None = None,
        proxy: ProxyType | None = None,
        timeout: Timeout = DEFAULT_TIMEOUT,
        limit: int = DEFAULT_LIMIT_SIMULTANEOUS_CONNECTIONS,
        ttl_dns_cache: int = DEFAULT_TTL_DNS_CACHE,
        **session_params: typing.Any,
    ) -> None:
        self.session = session
        self.limit = limit
        self.ttl_dns_cache = ttl_dns_cache
        self.session_params = session_params
        self._timeout = _get_client_timeout(timeout)
        self._proxy = proxy
        self._tcp_connector_kwargs = dict[str, typing.Any](
            ssl=ssl.create_default_context(cafile=certifi.where()),
            limit=limit,
            ttl_dns_cache=ttl_dns_cache,
        )
        self._tcp_connector_class: type[TCPConnector] = TCPConnector

        self.session_params.setdefault("headers", DEFAULT_HEADERS)
        self._setup_proxy()

    def __repr__(self) -> str:
        return "<{}: session={!r}, timeout={}, closed={}>".format(
            type(self).__name__,
            self.session,
            self._timeout,
            True if self.session is None else self.session.closed,
        )

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector._close()
            self.session._connector = None

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
        if not self.session:
            self.session = ClientSession(
                connector=self._tcp_connector_class(**self._tcp_connector_kwargs),
                json_serialize=json.dumps,
                **self.session_params,
            )

        async with self.session.request(
            method=method,
            url=url,
            data=data,
            timeout=self._timeout if timeout is None else _get_client_timeout(timeout),
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

    async def close(self, *, gracefully: bool = True) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

        if gracefully:
            # Wait 250 ms for graceful shutdown SSL connections
            await asyncio.sleep(0.250)

    def _setup_proxy(self) -> None:
        if self._proxy is not None:
            tcp_connector_class, data = _prepare_proxy_connector(self._proxy)
            self._tcp_connector_class = tcp_connector_class
            self._tcp_connector_kwargs.update(data if isinstance(data, dict) else dict(proxy_infos=data))


__all__ = ("AiohttpClient",)
