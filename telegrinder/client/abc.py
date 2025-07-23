import io
import typing
from abc import ABC, abstractmethod

from telegrinder.client.form_data import MultipartFormProto, encode_form_data

type Data = dict[str, typing.Any] | MultipartFormProto
type Files = dict[str, tuple[str, typing.Any]]


class ABCClient(ABC):
    CONNECTION_TIMEOUT_ERRORS: tuple[type[BaseException], ...] = ()
    CLIENT_CONNECTION_ERRORS: tuple[type[BaseException], ...] = ()

    @abstractmethod
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        pass

    @property
    @abstractmethod
    def timeout(self) -> float:
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> dict[str, typing.Any]:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def request_bytes(
        self,
        url: str,
        method: str = "GET",
        data: Data | None = None,
        **kwargs: typing.Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self, **kwargs: typing.Any) -> None:
        pass

    @classmethod
    @abstractmethod
    def multipart_form_factory(cls) -> MultipartFormProto:
        pass

    @classmethod
    def get_form(
        cls,
        *,
        data: dict[str, typing.Any],
        files: Files | None = None,
    ) -> MultipartFormProto:
        multipart_form = cls.multipart_form_factory()
        files = files or {}

        for k, v in encode_form_data(data, files).items():
            multipart_form.add_field(k, v)

        for n, (filename, content) in {
            k: (n, io.BytesIO(c) if isinstance(c, bytes) else c) for k, (n, c) in files.items()
        }.items():
            multipart_form.add_field(n, content, filename=filename)

        return multipart_form

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
