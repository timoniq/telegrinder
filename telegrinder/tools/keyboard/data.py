from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.abc import DictStrAny


@dataclasses.dataclass(kw_only=True, frozen=True)
class KeyboardModel:
    keyboard: typing.Iterable[typing.Iterable[DictStrAny]] = dataclasses.field(default_factory=lambda: [[]])
    resize_keyboard: bool = dataclasses.field(default=True)
    one_time_keyboard: bool = dataclasses.field(default=False)
    selective: bool = dataclasses.field(default=False)
    is_persistent: bool = dataclasses.field(default=False)
    input_field_placeholder: str | None = dataclasses.field(default=None)


__all__ = ("KeyboardModel",)
