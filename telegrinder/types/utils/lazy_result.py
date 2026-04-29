import typing

from kungfu.library.monad.result import Error, Ok, Result

_UNSET: typing.Final = object()


class LazyResult[T](Ok[T]):
    __slots__ = ("_factory", "_is_resolved")

    def __init__(self, factory: typing.Callable[[], T], /) -> None:
        self._factory = factory
        self._is_resolved = False
        super().__init__(typing.cast("T", _UNSET))

    def _resolve(self) -> T:
        if not self._is_resolved:
            self._value = self._factory()
            self._is_resolved = True

        return object.__getattribute__(self, "_value")

    def __getattribute__(self, name: str, /) -> typing.Any:
        if name == "_value":
            return object.__getattribute__(self, "_resolve")()
        return object.__getattribute__(self, name)


def lazy_result[T, R, E](
    result: Result[T, E],
    f: typing.Callable[[T], R],
    /,
) -> Result[R, E]:
    if isinstance(result, Error):
        return result

    return LazyResult(lambda: f(result.unwrap()))


__all__ = ("LazyResult", "lazy_result")
