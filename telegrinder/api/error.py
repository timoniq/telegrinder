class APIError(Exception):
    def __init__(self, code: int, error: str) -> None:
        self.code, self.error = code, error

    def __str__(self) -> str:
        return f"[{self.code}] {self.error}"

    def __repr__(self) -> str:
        return f"<APIError: {self.__str__()}>"


class InvalidTokenError(BaseException):
    pass


__all__ = ("APIError", "InvalidTokenError")
