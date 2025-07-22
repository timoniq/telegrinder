from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.abc import DictStrAny, RawKeyboard


class KeyboardParams(typing.TypedDict, total=False):
    is_persistent: bool
    one_time_keyboard: bool
    resize_keyboard: bool
    is_selective: bool
    input_field_placeholder: str | None


@dataclasses.dataclass(frozen=True)
class KeyboardModel:
    keyboard: RawKeyboard
    is_persistent: bool = dataclasses.field(default=False, kw_only=True)
    one_time_keyboard: bool = dataclasses.field(default=False, kw_only=True)
    resize_keyboard: bool = dataclasses.field(default=False, kw_only=True)
    is_selective: bool = dataclasses.field(default=False, kw_only=True)
    input_field_placeholder: str | None = dataclasses.field(default=None, kw_only=True)

    def dict(self) -> DictStrAny:
        dct = dataclasses.asdict(self)
        dct["keyboard"] = [row for row in self.keyboard if row]
        return dct


__all__ = ("KeyboardModel", "KeyboardParams")
