from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.abc import DictStrAny


@dataclasses.dataclass(kw_only=True, frozen=True)
class KeyboardModel:
    resize_keyboard: bool
    one_time_keyboard: bool
    selective: bool
    is_persistent: bool
    keyboard: typing.Iterable[typing.Iterable[DictStrAny]]


__all__ = ("KeyboardModel",)
