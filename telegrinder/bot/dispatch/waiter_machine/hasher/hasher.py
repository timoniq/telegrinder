import typing

from fntypes import Option

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.tools.functional import from_optional

Event = typing.TypeVar("Event", bound=BaseCute)
Data = typing.TypeVar("Data")


ECHO = lambda x: x


class Hasher(typing.Generic[Event, Data]):
    def __init__(
        self,
        view: type[BaseView[Event]],
        create_hash: typing.Callable[[Data], typing.Hashable | None] | None = None,
        get_data_from_event: typing.Callable[[Event], Data | None] | None = None,
    ):
        self.view = view
        self._create_hash = create_hash
        self._get_data_from_event = get_data_from_event

    def get_name(self) -> str:
        return f"{self.view.__class__.__name__}_{id(self)}"

    def create_hash(self, data: Data) -> Option[typing.Hashable]:
        if self._create_hash is None:
            raise NotImplementedError
        return from_optional(self._create_hash(data))

    def get_data_from_event(self, event: Event) -> Option[Data]:
        if not self._get_data_from_event:
            raise NotImplementedError
        return from_optional(self._get_data_from_event(event))

    def create_hash_from_event(self, event: Event) -> Option[typing.Hashable]:
        return self.get_data_from_event(event).and_then(self.create_hash)

    def __hash__(self) -> int:
        return hash(self.get_name())

    def __repr__(self) -> str:
        return f"<Hasher {self.get_name()}>"
