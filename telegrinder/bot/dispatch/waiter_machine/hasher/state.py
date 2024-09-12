from fntypes.option import Option

from telegrinder.bot.dispatch.view import BaseStateView
from telegrinder.bot.dispatch.waiter_machine.hasher.hasher import ECHO, Event, Hasher
from telegrinder.tools.functional import from_optional


class StateViewHasher(Hasher[Event, int]):
    view: BaseStateView[Event]

    def __init__(self, view: type[BaseStateView[Event]]) -> None:
        super().__init__(view, get_hash_from_data=ECHO)

    def get_data_from_event(self, event: Event) -> Option[int]:
        return from_optional(self.view.get_state_key(event))


__all__ = ("StateViewHasher",)
