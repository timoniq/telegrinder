import typing


class CatcherError(TypeError):
    def __init__(self, exc: typing.Any, error: str) -> None:
        self.exc = exc
        self.error = error


__all__ = ("CatcherError",)
