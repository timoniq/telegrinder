import typing

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.handler.abc import ABCHandler

type OnDrop[Event: BaseCute[typing.Any] = typing.Any] = typing.Callable[..., typing.Awaitable[typing.Any] | typing.Any]


class WaiterActions[Event: BaseCute[typing.Any] = typing.Any](typing.TypedDict):
    on_miss: typing.NotRequired[ABCHandler]
    on_drop: typing.NotRequired[OnDrop[Event]]


__all__ = ("WaiterActions",)
