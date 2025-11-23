from __future__ import annotations

import secrets
import typing

from fntypes.library.misc import from_optional
from fntypes.library.monad.option import Option

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.view.base import View

type HasherWithData[Event: BaseCute, Data] = tuple[Hasher[Event, Data], View, Data]

Event = typing.TypeVar("Event", bound=BaseCute, covariant=True)
Data = typing.TypeVar("Data", covariant=True)


def ECHO[T](__x: T) -> T:  # noqa
    return __x


class Hasher(typing.Generic[Event, Data]):
    def __init__(
        self,
        get_hash_from_data: typing.Callable[[Data], typing.Hashable | None] | None = None,
        get_data_from_event: typing.Callable[[Event], Data | None] | None = None,
    ) -> None:
        self.code = secrets.token_hex(8)
        self._get_hash_from_data = get_hash_from_data
        self._get_data_from_event = get_data_from_event

    def __call__[D](
        self: Hasher[Event, D],
        view: View,
        data: D,
        /,
    ) -> HasherWithData[Event, D]:
        return (self, view, data)

    def __hash__(self) -> int:
        return hash(self.code)

    def __repr__(self) -> str:
        return f"<Hasher {self.code}>"

    def get_hash_from_data[D](self: Hasher[Event, D], data: D) -> Option[typing.Hashable]:
        if self._get_hash_from_data is None:
            raise NotImplementedError
        return from_optional(self._get_hash_from_data(data))

    def get_data_from_event[E: BaseCute](self: Hasher[E, Data], event: E) -> Option[Data]:
        if not self._get_data_from_event:
            raise NotImplementedError
        return from_optional(self._get_data_from_event(event))

    def get_hash_from_data_from_event[E: BaseCute](
        self: Hasher[E, Data],
        event: E,
    ) -> Option[typing.Hashable]:
        return self.get_data_from_event(event).then(self.get_hash_from_data)


__all__ = ("Hasher",)
