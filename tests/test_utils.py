import typing
from http import HTTPStatus

from telegrinder.api.api import API, Token
from telegrinder.client.abc import ABCClient, Response


class MockedHttpClient(ABCClient):
    def __init__(
        self,
        return_value: typing.Any | None = None,
        callback: typing.Callable | None = None,
    ) -> None:
        super().__init__()
        self.return_value = return_value
        self.callback = callback or (lambda method, url, data: None)

    @property
    def timeout(self) -> float:
        return 0.0

    async def request(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> Response:
        response = self.return_value or self.callback(method, url, data)
        content = response if isinstance(response, bytes) else b""
        return Response(response=response, content=content, status=HTTPStatus.OK)

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs,
    ) -> str | typing.Any:
        return (await self.request(url, method, data, **kwargs)).response

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any] | typing.Any:
        return (await self.request(url, method, data, **kwargs)).response

    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> bytes | typing.Any:
        return (await self.request(url, method, data, **kwargs)).response

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> bytes | typing.Any:
        return (await self.request(url, method, data, **kwargs)).response

    @classmethod
    def multipart_form_builder(cls) -> typing.Any:
        pass

    @classmethod
    def get_form(
        cls,
        data: dict[str, typing.Any],
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> typing.Any:
        pass

    async def close(self) -> None:
        pass


def with_mocked_api(return_value: typing.Any):
    def decorator(func: typing.Callable):
        async def wrapper(*args, **kwargs):
            api = API(Token("123:ABCdef"), http=MockedHttpClient(return_value))
            return await func(*args, **kwargs, api=api)

        return wrapper

    return decorator
