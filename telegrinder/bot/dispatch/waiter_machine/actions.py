import typing

from telegrinder.bot.dispatch.handler.abc import ABCHandler

from .short_state import EventModel, ShortState


class WaiterActions(typing.TypedDict, typing.Generic[EventModel]):
    on_miss: typing.NotRequired[ABCHandler[EventModel]]
    on_drop: typing.NotRequired[typing.Callable[[ShortState[EventModel]], None]]
