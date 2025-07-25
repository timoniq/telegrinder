import typing
from functools import cached_property
from http import HTTPStatus

from fntypes.library.misc import from_optional
from fntypes.library.monad.option import Option


class ReprErrorMixin:
    def __repr__(self) -> str:
        return f"{type(self).__name__}: {self}"


class APIError(ReprErrorMixin, Exception):
    def __init__(
        self,
        code: int,
        error: str,
        data: dict[str, typing.Any],
    ) -> None:
        self.code, self.error, self.parameters = code, error, data

    @cached_property
    def status_code(self) -> HTTPStatus:
        return HTTPStatus(self.code)

    @property
    def retry_after(self) -> Option[int]:
        return from_optional(self.parameters.get("retry_after"))

    @property
    def migrate_to_chat_id(self) -> Option[int]:
        return from_optional(self.parameters.get("migrate_to_chat_id"))

    def __str__(self) -> str:
        return f"[{self.code}] ({self.status_code.name}) {self.error}"


class APIServerError(ReprErrorMixin, Exception):
    def __init__(self, message: str, retry_after: int) -> None:
        self.message = message
        self.retry_after = retry_after
        super().__init__(message)


class InvalidTokenError(BaseException):
    pass


__all__ = ("APIError", "APIServerError", "InvalidTokenError")
