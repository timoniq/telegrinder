import typing
from functools import cached_property

from fntypes.option import Option

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.tools.functional import from_optional

T = typing.TypeVar("T")
Event = typing.TypeVar("Event", bound=BaseCute)
Data = typing.TypeVar("Data")


def _echo(__x: T) -> T:
    return __x


ECHO = _echo


class Hasher(typing.Generic[Event, Data]):
    def __init__(
        self,
        view: type[BaseView[Event]],
        get_hash_from_data: typing.Callable[[Data], typing.Hashable | None] | None = None,
        get_data_from_event: typing.Callable[[Event], Data | None] | None = None,
    ) -> None:
        self.view = view
        self._get_hash_from_data = get_hash_from_data
        self._get_data_from_event = get_data_from_event

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Hasher {self.name}>"

    @cached_property
    def name(self) -> str:
        return f"{self.view.__class__.__name__}_{id(self)}"

    def get_hash_from_data(self, data: Data) -> Option[typing.Hashable]:
        if self._get_hash_from_data is None:
            raise NotImplementedError
        return from_optional(self._get_hash_from_data(data))

    def get_data_from_event(self, event: Event) -> Option[Data]:
        if not self._get_data_from_event:
            raise NotImplementedError
        return from_optional(self._get_data_from_event(event))

    def get_hash_from_data_from_event(self, event: Event) -> Option[typing.Hashable]:
        return self.get_data_from_event(event).and_then(self.get_hash_from_data)  # type: ignore


__all__ = ("Hasher",)