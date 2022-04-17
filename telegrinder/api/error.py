import typing


class APIError(BaseException):
    def __init__(self, code: int, error: typing.Optional[str] = None):
        self.code, self.error = code, error
