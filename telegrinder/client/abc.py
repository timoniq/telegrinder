import typing
from abc import ABC, abstractmethod

from telegrinder.client.form_data import MultipartFormProto, encode_form_data

type Data = dict[str, typing.Any] | MultipartFormProto


class ABCClient[MultipartForm: MultipartFormProto](ABC):
    CONNECTION_TIMEOUT_ERRORS: tuple[type[BaseException], ...] = ()
    CLIENT_CONNECTION_ERRORS: tuple[type[BaseException], ...] = ()

    @abstractmethod
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
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
    async def close(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def multipart_form_factory(cls) -> MultipartForm:
        pass

    @classmethod
    def get_form(
        cls,
        *,
        data: dict[str, typing.Any],
        files: dict[str, tuple[str, typing.Any]] | None = None,
    ) -> MultipartForm:
        files = files or {}
        multipart_form = cls.multipart_form_factory()

        for k, v in encode_form_data(data, files).items():
            multipart_form.add_field(k, v)

        for n, (filename, content) in files.items():
            multipart_form.add_field(n, content, filename=filename)

        return multipart_form

    async def __aenter__(self) -> typing.Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: typing.Any,
        exc_tb: typing.Any,
    ) -> bool:
        await self.close()
        return not bool(exc_val)


__all__ = ("ABCClient",)
