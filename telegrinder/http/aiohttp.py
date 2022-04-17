import typing
from telegrinder.http.abc import ABCClient
from aiohttp import ClientSession, TCPConnector
from telegrinder.modules import json, JSONModule

if typing.TYPE_CHECKING:
    from aiohttp import ClientResponse


class AiohttpClient(ABCClient):
    def __init__(
        self,
        loop: typing.Optional[ClientSession] = None,
        session: typing.Optional[ClientSession] = None,
        json_processing_module: typing.Optional[JSONModule] = None,
        **session_params
    ):
        self.loop = loop
        self.session = session
        self.json_processing_module = json_processing_module or json
        self.session_params = session_params

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> "ClientResponse":
        if not self.session:
            self.session = ClientSession(
                connector=TCPConnector(ssl=False),
                json_serialize=self.json_processing_module.dumps,
                **self.session_params,
            )
        async with self.session.request(
            url=url, method=method, data=data, **kwargs
        ) as response:
            await response.read()
            return response

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8", loads=self.json_processing_module.loads, content_type=None
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def __del__(self):
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None
