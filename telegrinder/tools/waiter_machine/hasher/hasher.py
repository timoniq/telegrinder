import dataclasses
import secrets
import typing
from functools import cached_property

from kungfu.library.monad.option import NOTHING, Option, Some

from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types import BaseCute
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.tools.waiter_machine.machine import HasherWithData, HasherWithViewAndData

type HasherFromData[Data] = typing.Callable[[Data], typing.Hashable | None]
type DataFromEvent[Event, Data] = typing.Callable[[Event], Data | None]

Event = typing.TypeVar("Event", bound="BaseCute", covariant=True, default=typing.Any)
Data = typing.TypeVar("Data", covariant=True, default=typing.Any)

_NOVIEW: typing.Final[typing.Any] = object()


def _from_optional(x: typing.Any, /) -> Option[typing.Any]:
    return Some(x) if x is not None else NOTHING


@dataclasses.dataclass(kw_only=True, frozen=True, repr=False)
class Hasher(typing.Generic[Event, Data]):
    update_types: frozenset[UpdateType]
    hash_from_data: HasherFromData[Data] | None = dataclasses.field(default=None)
    data_from_event: DataFromEvent[Event, Data] | None = dataclasses.field(default=None)
    code: str = dataclasses.field(
        init=False,
        default_factory=lambda: secrets.token_hex(8),
    )

    @typing.overload
    def __call__[HasherData](
        self: Hasher[Event, HasherData], data: HasherData, /
    ) -> HasherWithData[Event, HasherData]: ...

    @typing.overload
    def __call__[HasherData, ViewType: View](
        self: Hasher[Event, HasherData],
        view: ViewType,
        data: HasherData,
        /,
    ) -> HasherWithViewAndData[Event, ViewType, HasherData]: ...

    def __call__(self, data: typing.Any, view: typing.Any = _NOVIEW, /) -> tuple[typing.Any, ...]:
        return (self, view, data) if view is not _NOVIEW else (self, data)

    def __hash__(self) -> int:
        return self.hash

    def __repr__(self) -> str:
        return f"<Hasher {self.code}>"

    @cached_property
    def hash(self) -> int:
        return hash(self.code)

    def get_hash_from_data[D](self: Hasher[Event, D], data: D) -> Option[typing.Hashable]:
        if self.hash_from_data is None:
            raise NotImplementedError
        return _from_optional(self.hash_from_data(data))

    def get_data_from_event[E: BaseCute](self: Hasher[E, Data], event: E) -> Option[Data]:
        if not self.data_from_event:
            raise NotImplementedError
        return _from_optional(self.data_from_event(event))

    def get_hash_from_data_from_event[E: BaseCute](
        self: Hasher[E, Data],
        event: E,
    ) -> Option[typing.Hashable]:
        return self.get_data_from_event(event).then(self.get_hash_from_data)


__all__ = ("Hasher",)
