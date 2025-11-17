from __future__ import annotations

import typing

from telegrinder.bot.dispatch.handler.abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.waiter_machine.short_state import ShortState

type OnDrop[Event: BaseCute[typing.Any] = typing.Any] = typing.Callable[
    typing.Concatenate[ShortState[Event], ...],
    typing.Awaitable[typing.Any] | typing.Any,
]


class WaiterActions[Event: BaseCute[typing.Any] = typing.Any](typing.TypedDict):
    on_miss: typing.NotRequired[ABCHandler]
    on_drop: typing.NotRequired[OnDrop[Event]]


__all__ = ("WaiterActions",)
