class ComposeError(BaseException):
    def __init__(self, message: str = "<no error description>", /) -> None:
        self.message = message
        super().__init__(message)


__all__ = ("ComposeError",)
