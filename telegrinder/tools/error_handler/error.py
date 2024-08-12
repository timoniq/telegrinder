class CatcherError(BaseException):
    __slots__ = ("exc", "message")

    def __init__(self, exc: BaseException, message: str) -> None:
        self.exc = exc
        self.message = message


__all__ = ("CatcherError",)
