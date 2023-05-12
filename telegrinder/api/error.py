import typing


class APIError(BaseException):
    def __init__(self, code: int, error: str | None = None):
        self.code, self.error = code, error
