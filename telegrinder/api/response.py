from telegrinder.model import Model
from telegrinder.result import Result
from telegrinder.api.error import APIError
import msgspec


class APIResponse(Model):
    ok: bool
    result: msgspec.Raw = b""
    error_code: int = 0
    description: str = ""

    def to_result(self) -> Result[msgspec.Raw, APIError]:
        if self.ok:
            return Result(True, value=self.result)
        return Result(False, error=APIError(self.error_code, self.description))
