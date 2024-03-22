import typing
from abc import ABC, abstractmethod


class ABCClient(ABC):
    @abstractmethod
    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, typing.Any] | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_form(
        cls,
        data: dict[str, typing.Any],
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> typing.Any:
        pass

    async def __aenter__(self) -> typing.Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: typing.Any,
        exc_tb: typing.Any,
    ) -> None:
        await self.close()


__all__ = ("ABCClient",)
