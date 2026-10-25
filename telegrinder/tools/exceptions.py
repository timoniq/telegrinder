import typing


def iter_exceptions(exceptions: typing.Iterable[BaseException], /) -> typing.Iterator[BaseException]:
    for exception in exceptions:
        yield exception

        if isinstance(exception, BaseExceptionGroup):
            yield from iter_exceptions(exception.exceptions)


__all__ = ("iter_exceptions",)
