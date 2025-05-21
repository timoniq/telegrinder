import typing
from functools import cached_property
from http import HTTPStatus

from fntypes.option import Nothing, Option, Some


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
        super().__init__(code, error, data)

    @cached_property
    def status_code(self) -> HTTPStatus:
        return HTTPStatus(self.code)

    @property
    def retry_after(self) -> Option[int]:
        return Some(v) if (v := self.parameters.get("retry_after")) is not None else Nothing()

    def __str__(self) -> str:
        return f"[{self.code}] ({self.status_code.name}) {self.error}"


class APIServerError(ReprErrorMixin, Exception):
    def __init__(self, message: str, retry_after: int) -> None:
        self.message = message
        self.retry_after = retry_after
        super().__init__(message, retry_after)

    def __str__(self) -> str:
        return self.message


class InvalidTokenError(BaseException):
    pass


__all__ = ("APIError", "APIServerError", "InvalidTokenError")
