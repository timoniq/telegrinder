import dataclasses

from telegrinder.tools.keyboard.base import BaseKeyboard, DictStrAny
from telegrinder.types.objects import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


@dataclasses.dataclass(kw_only=True)
class Keyboard(BaseKeyboard):
    resize_keyboard: bool = dataclasses.field(default=True)
    one_time_keyboard: bool = dataclasses.field(default=False)
    selective: bool = dataclasses.field(default=False)
    is_persistent: bool = dataclasses.field(default=False)
    keyboard: list[list[DictStrAny]] = dataclasses.field(
        default_factory=lambda: [[]],
        init=False,
    )

    def dict(self) -> DictStrAny:
        self.keyboard = [row for row in self.keyboard if row]
        return dataclasses.asdict(self)

    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(**self.dict())

    def get_settings(self) -> DictStrAny:
        return {
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard,
            "selective": self.selective,
            "is_persistent": self.is_persistent,
        }

    def get_keyboard_remove(self) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove.from_data(
            remove_keyboard=True,
            selective=self.selective,
        )


class InlineKeyboard(BaseKeyboard):
    def __init__(self) -> None:
        self.keyboard = [[]]

    def dict(self) -> DictStrAny:
        return dict(inline_keyboard=[row for row in self.keyboard if row])

    def get_settings(self) -> DictStrAny:
        return {}

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(**self.dict())


__all__ = ("InlineKeyboard", "Keyboard")
