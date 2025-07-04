import typing

import msgspec
from fntypes.result import Error, Ok, Result

from telegrinder.api.error import APIError
from telegrinder.model import Model


class APIResponse(Model):
    ok: bool = False
    result: msgspec.Raw = msgspec.Raw(b"")
    error_code: int = 400
    description: str = "Something went wrong"
    parameters: dict[str, typing.Any] = msgspec.field(default_factory=dict[str, typing.Any])

    def to_result(self) -> Result[msgspec.Raw, APIError]:
        if self.ok:
            return Ok(self.result)
        return Error(APIError(code=self.error_code, error=self.description, data=self.parameters))


__all__ = ("APIResponse",)
