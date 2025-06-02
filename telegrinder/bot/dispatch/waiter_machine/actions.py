import typing

from telegrinder.bot.dispatch.handler.abc import ABCHandler

from .short_state import ShortState

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute


class WaiterActions[Event: BaseCute[typing.Any]](typing.TypedDict):
    on_miss: typing.NotRequired[ABCHandler]
    on_drop: typing.NotRequired[typing.Callable[[ShortState], None]]


__all__ = ("WaiterActions",)
