import msgspec

from telegrinder.model import Model
from telegrinder.result import Result, Ok, Error
from telegrinder.api.error import APIError


class APIResponse(Model):
    ok: bool = False
    result: msgspec.Raw = msgspec.Raw(b"")
    error_code: int = 0
    description: str = ""

    def to_result(self) -> Result[msgspec.Raw, APIError]:
        if self.ok:
            return Ok(self.result)
        return Error(APIError(self.error_code, self.description))
      
