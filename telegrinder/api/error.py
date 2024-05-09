class APIError(BaseException):
    def __init__(self, code: int, error: str | None = None) -> None:
        self.code, self.error = code, error

    def __str__(self) -> str:
        return f"[{self.code}] {self.error or 'Something went wrong'}"

    def __repr__(self) -> str:
        return f"<APIError: {self.__str__()}>"


class InvalidTokenError(BaseException): ...


__all__ = ("APIError", "InvalidTokenError")
