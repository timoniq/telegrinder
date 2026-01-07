from __future__ import annotations

import typing
from abc import ABC, abstractmethod

from telegrinder.client.form_data import MultipartBuilderProto, encode_form_data

if typing.TYPE_CHECKING:
    import datetime

type Data = typing.Any
type Files = dict[str, tuple[str, typing.Any]]
type Timeout = int | float | datetime.timedelta


class ABCClient(ABC):
    CONNECTION_TIMEOUT_ERRORS: tuple[type[BaseException], ...] = ()
    CLIENT_CONNECTION_ERRORS: tuple[type[BaseException], ...] = ()

    @abstractmethod
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        pass

    @property
    @abstractmethod
    def timeout(self) -> datetime.timedelta:
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        timeout: Timeout | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self, **kwargs: typing.Any) -> None:
        pass

    @classmethod
    @abstractmethod
    def multipart_form_builder(cls) -> MultipartBuilderProto:
        pass

    @classmethod
    def get_form(
        cls,
        *,
        data: dict[str, typing.Any] | None = None,
        files: Files | None = None,
    ) -> typing.Any:
        builder = cls.multipart_form_builder()

        if not data and not files:
            return builder.build()

        data = data or {}
        files = files or {}

        for k, v in encode_form_data(data, files).items():
            builder.add_field(k, v)

        for n, (filename, content) in files.items():
            builder.add_field(n, content, filename=filename)

        return builder.build()

    async def __aenter__(self) -> typing.Self:
        return self

    async def __aexit__(
        self,
        exc_type: typing.Any,
        exc_val: typing.Any,
        exc_tb: typing.Any,
    ) -> None:
        await self.close()


__all__ = ("ABCClient",)
