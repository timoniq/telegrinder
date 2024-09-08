from fntypes import Option

from telegrinder.bot.dispatch.view import BaseStateView
from telegrinder.tools.functional import from_optional

from .hasher import ECHO, Event, Hasher


class StateViewHasher(Hasher[Event, int]):
    view: BaseStateView

    def __init__(self, view: type[BaseStateView[Event]]):
        super().__init__(view, get_hash_from_data=ECHO)

    def get_data_from_event(self, event: Event) -> Option[int]:
        return from_optional(self.view.get_state_key(event))


__all__ = ("StateViewHasher",)
