class APIError(BaseException):
    def __init__(self, code: int, error: str | None = None):
        self.code, self.error = code, error
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.error}"

    def __repr__(self) -> str:
        return f"<APIError [{self.code}] {self.error}>"


class InvalidTokenError(BaseException):
    ...
