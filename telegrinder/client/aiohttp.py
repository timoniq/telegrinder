import secrets
import ssl
import typing

import aiohttp
import certifi
from aiohttp import ClientSession, TCPConnector

from telegrinder.client.abc import ABCClient
from telegrinder.modules import JSONModule, json

if typing.TYPE_CHECKING:
    from aiohttp import ClientResponse


class AiohttpClient(ABCClient):
    def __init__(
        self,
        session: ClientSession | None = None,
        json_processing_module: JSONModule | None = None,
        timeout: aiohttp.ClientTimeout | None = None,
        **session_params: typing.Any,
    ) -> None:
        self.session = session
        self.json_processing_module = json_processing_module or json
        self.session_params = session_params
        self.timeout = timeout or aiohttp.ClientTimeout(total=0)
    
    def __repr__(self) -> str:
        return "<{}: session={!r}, timeout={}, closed={}>".format(
            self.__class__.__name__,
            self.session,
            self.timeout,
            False if self.session is None else self.session.closed,
        )
    
    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> "ClientResponse":
        if not self.session:
            self.session = ClientSession(
                connector=TCPConnector(
                    ssl=ssl.create_default_context(cafile=certifi.where())
                ),
                json_serialize=self.json_processing_module.dumps,
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
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8",
            loads=self.json_processing_module.loads,
            content_type=None,
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | aiohttp.FormData | None = None,
        **kwargs: typing.Any,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)  # type: ignore
        return await response.text(encoding="utf-8")

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | aiohttp.FormData | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)  # type: ignore
        if response._body is None:
            await response.read()
        return response._body

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    @classmethod
    def get_form(
        cls,
        data: dict[str, typing.Any],
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> aiohttp.formdata.FormData:
        files = files or {}
        form = aiohttp.formdata.FormData(quote_fields=False)
        for k, v in data.items():
            form.add_field(k, str(v))
        
        for n, f in files.items():
            form.add_field(n, f[1], filename=f[0])
        
        return form

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None


__all__ = ("AiohttpClient",)
