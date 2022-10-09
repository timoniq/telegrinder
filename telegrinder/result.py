import typing

T = typing.TypeVar("T")
E = typing.TypeVar("E")


class Result(typing.Generic[T, E]):
    def __init__(
        self,
        is_ok: bool,
        *,
        value: typing.Optional[T] = None,
        error: typing.Optional[E] = None
    ):
        self.is_ok = is_ok
        self.value = value
        self.error = error

    def unwrap(self) -> T:
        if not self.is_ok:
            raise self.error
        return self.value

    def unwrap_or(self, alternate_value: T):
        if not self.is_ok:
            return alternate_value
        return self.value

    def unwrap_via_handler(
        self, handler: typing.Callable[["Result", dict], T], ctx: dict
    ):
        return handler(self, ctx)

    def __repr__(self):
        return "<Result ({}: {})>".format(
            "Ok" if self.is_ok else "Error",
            repr(self.value if self.is_ok else self.error),
        )
