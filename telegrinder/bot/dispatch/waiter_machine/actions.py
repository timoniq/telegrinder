import typing

from telegrinder.bot.dispatch.handler.abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute

type OnDrop[Event: BaseCute[typing.Any] = typing.Any] = typing.Callable[..., typing.Awaitable[typing.Any] | typing.Any]


class WaiterActions[Event: BaseCute[typing.Any] = typing.Any](typing.TypedDict):
    on_miss: typing.NotRequired[ABCHandler]
    on_drop: typing.NotRequired[OnDrop[Event]]


__all__ = ("WaiterActions",)
