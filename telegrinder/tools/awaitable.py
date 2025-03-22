import typing
from inspect import isawaitable


async def maybe_awaitable[T](obj: T | typing.Awaitable[T], /) -> T:
    if isawaitable(obj):
        return await obj
    return obj


__all__ = ("maybe_awaitable",)
