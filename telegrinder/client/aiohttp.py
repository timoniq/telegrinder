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
        **session_params
    ):
        self.session = session
        self.json_processing_module = json_processing_module or json
        self.session_params = session_params
        self.timeout = timeout or aiohttp.ClientTimeout(total=0)

    async def request_raw(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs
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
            url=url, method=method, data=data, timeout=self.timeout, **kwargs
        ) as response:
            await response.read()
            return response

    async def request_json(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8", loads=self.json_processing_module.loads, content_type=None
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict | aiohttp.FormData | None = None,
        **kwargs
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: dict | aiohttp.FormData | None = None,
        **kwargs
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        if response._body is None:
            await response.read()
        return response._body

    async def request_content(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    @classmethod
    def get_form(cls, data: dict) -> aiohttp.formdata.FormData:
        form = aiohttp.formdata.FormData(quote_fields=False)
        for k, v in data.items():
            params = {}
            if isinstance(v, tuple):
                params["filename"], v = v[0], v[1]
            else:
                v = str(v)
            form.add_field(k, v, **params)
        return form

    def __del__(self):
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None
