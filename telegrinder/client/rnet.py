
import dataclasses
import pathlib
import sys
import typing

import certifi
import rnet
import rnet.exceptions
from rnet import Method as HTTPMethod

from telegrinder.__meta__ import __version__
from telegrinder.client.abc import ABCClient
from telegrinder.modules import json

if typing.TYPE_CHECKING:
    from rnet import ClientParams, Request

type Data = dict[str, typing.Any] | rnet.Multipart
type Method = typing.Literal["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"]

_METHODS_MAP: typing.Final[dict[Method, HTTPMethod]] = {
    "GET": HTTPMethod.GET,
    "HEAD": HTTPMethod.HEAD,
    "POST": HTTPMethod.POST,
    "PUT": HTTPMethod.PUT,
    "DELETE": HTTPMethod.DELETE,
    "OPTIONS": HTTPMethod.OPTIONS,
    "TRACE": HTTPMethod.TRACE,
    "PATCH": HTTPMethod.PATCH,
}
USER_AGENT: typing.Final = "CPython/{}.{} RNET/3 Telegrinder/{}".format(
    sys.version_info.major,
    sys.version_info.minor,
    __version__,
)
DEFAULT_CONNECTION_TIMEOUT: typing.Final = 30
DEFAULT_READ_TIMEOUT: typing.Final = 30
DEFAULT_TIMEOUT: typing.Final = 30
DEFAULT_HTTP2_MAX_RETRIES: typing.Final = 10
DEFAULT_ZSTD: typing.Final = True
DEFAULT_VERIFY: typing.Final = pathlib.Path(certifi.where())
DEFAULT_ALLOW_REDIRECTS: typing.Final = True
DEFAULT_HTTP2_ONLY: typing.Final = True
DEFAULT_TCP_KEEPALIVE_TIME: typing.Final = 60
DEFAULT_TCP_KEEPALIVE_INTERVAL: typing.Final = 15
DEFAULT_TCP_KEEPALIVE_RETRIES: typing.Final = 4
DEFAULT_TCP_USER_TIMEOUT: typing.Final = (
    DEFAULT_TCP_KEEPALIVE_TIME + DEFAULT_TCP_KEEPALIVE_INTERVAL * DEFAULT_TCP_KEEPALIVE_RETRIES
)
DEFAULT_TCP_REUSEADDR: typing.Final = True
DEFAULT_CONNECTION_POOL_IDLE_TIMEOUT: typing.Final = 60
DEFAULT_CONNECTION_POOL_CONNECTIONS: typing.Final = 32
CONNECTION_POOL_MAX_SIZE: typing.Final = DEFAULT_CONNECTION_POOL_CONNECTIONS * 2


@dataclasses.dataclass(frozen=True, slots=True)
class RnetMultipartBuilder:
    parts: list[rnet.Part] = dataclasses.field(default_factory=list[rnet.Part])

    def add_field(
        self,
        name: str,
        value: typing.Any,
        /,
        *,
        filename: str | None = None,
    ) -> None:
        self.parts.append(rnet.Part(name, value, filename=filename))

    def build(self) -> rnet.Multipart:
        return rnet.Multipart(*self.parts)


class RnetClient(ABCClient):
    __slots__ = ("_timeout", "_client")

    CONNECTION_TIMEOUT_ERRORS: typing.ClassVar = (
        rnet.exceptions.TimeoutError,
        rnet.exceptions.RustPanic,
    )
    CLIENT_CONNECTION_ERRORS: typing.ClassVar = (
        rnet.exceptions.ConnectionError,
        rnet.exceptions.ConnectionResetError,
        rnet.exceptions.TlsError,
        rnet.exceptions.DNSResolverError,
        rnet.exceptions.RustPanic,
    )

    def __init__(self, **params: typing.Unpack[ClientParams]) -> None:
        params.setdefault("connect_timeout", DEFAULT_CONNECTION_TIMEOUT)
        params.setdefault("read_timeout", DEFAULT_READ_TIMEOUT)
        params.setdefault("verify", DEFAULT_VERIFY)
        params.setdefault("http2_only", DEFAULT_HTTP2_ONLY)
        params.setdefault("allow_redirects", DEFAULT_ALLOW_REDIRECTS)
        params.setdefault("zstd", DEFAULT_ZSTD)
        params.setdefault("tcp_keepalive", DEFAULT_TCP_KEEPALIVE_TIME)
        params.setdefault("tcp_keepalive_interval", DEFAULT_TCP_KEEPALIVE_INTERVAL)
        params.setdefault("tcp_keepalive_retries", DEFAULT_TCP_KEEPALIVE_RETRIES)
        params.setdefault("tcp_user_timeout", DEFAULT_TCP_USER_TIMEOUT)
        params.setdefault("tcp_reuse_address", DEFAULT_TCP_REUSEADDR)
        params.setdefault("pool_idle_timeout", DEFAULT_CONNECTION_POOL_IDLE_TIMEOUT)
        params.setdefault("pool_max_idle_per_host", DEFAULT_CONNECTION_POOL_CONNECTIONS)
        params.setdefault("pool_max_size", CONNECTION_POOL_MAX_SIZE)

        self._timeout = params.setdefault("timeout", DEFAULT_TIMEOUT)
        self._client = rnet.Client(**params)

    def __repr__(self) -> str:
        return "<{}: client={!r}, timeout={}>".format(
            type(self).__name__,
            self._client,
            self._timeout,
        )

    @property
    def timeout(self) -> float:
        return self._timeout

    @classmethod
    def multipart_form_builder(cls) -> RnetMultipartBuilder:
        return RnetMultipartBuilder()

    async def request(
        self,
        url: str,
        method: Method,
        data: Data | None = None,
        **kwargs: typing.Unpack[Request],
    ) -> rnet.Response:
        kwargs.setdefault("version", rnet.Version.HTTP_2)
        kwargs.setdefault("zstd", DEFAULT_ZSTD)

        if data is not None:
            if isinstance(data, rnet.Multipart):
                kwargs["multipart"] = data
            elif isinstance(data, dict):
                kwargs["json"] = data

        if (json_body := kwargs.pop("json", None)) is not None:
            kwargs["body"] = json.dumps(json_body)

        return await self._client.request(_METHODS_MAP[method], url, **kwargs)

    async def request_text(
        self,
        *,
        url: str,
        method: Method = "GET",
        data: Data | None = None,
        **kwargs: typing.Unpack[Request],
    ) -> str:
        return await (await self.request(url, method, data=data, **kwargs)).text_with_charset(encoding="utf-8")

    async def request_bytes(
        self,
        *,
        url: str,
        method: Method = "GET",
        data: Data | None = None,
        **kwargs: typing.Unpack[Request],
    ) -> bytes:
        return await (await self.request(url, method, data=data, **kwargs)).bytes()

    async def request_content(
        self,
        *,
        url: str,
        method: Method = "GET",
        data: Data | None = None,
        **kwargs: typing.Unpack[Request],
    ) -> bytes:
        return await self.request_bytes(url=url, method=method, data=data, **kwargs)

    async def request_json(
        self,
        *,
        url: str,
        method: Method = "GET",
        data: Data | None = None,
        **kwargs: typing.Unpack[Request],
    ) -> dict[str, typing.Any]:
        return json.loads(await self.request_bytes(url=url, method=method, data=data, **kwargs))

    async def close(self) -> None:
        return None


__all__ = ("RnetClient", "RnetMultipartBuilder")
