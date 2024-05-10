class CatcherError(BaseException):
    def __init__(self, exc: BaseException, message: str) -> None:
        self.exc = exc
        self.message = message


__all__ = ("CatcherError",)
