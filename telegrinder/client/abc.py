from abc import ABC, abstractmethod
import typing


class ABCClient(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> bytes:
        pass

    @abstractmethod
    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
