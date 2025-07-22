from __future__ import annotations

import typing
from functools import cache

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.button import ButtonRule
    from telegrinder.tools.keyboard.abc import ABCKeyboard, RawKeyboard
    from telegrinder.tools.keyboard.base import BaseKeyboard
    from telegrinder.tools.keyboard.button import BaseButton


@cache
def get_keyboard_button_rules(
    keyboard_class: type[ABCKeyboard], /
) -> dict[str, ButtonRule[BaseButton[typing.Any]]]:
    from telegrinder.bot.rules.button import ButtonRule

    return {
        name: ButtonRule(button=button, rule=button.rule)
        for name, button in dict(vars(keyboard_class)).items()
        if isinstance(button, keyboard_class.__button_class__) and not is_dunder(name)
    }


def is_dunder(name: str, /) -> bool:
    return name.startswith("__") and name.endswith("__")


def copy_keyboard(keyboard: RawKeyboard, /) -> RawKeyboard:
    return [row.copy() for row in keyboard if row]


def freaky_keyboard_merge[T: BaseKeyboard](
    button: BaseButton[T],
    keyboard_or_button: T | BaseButton[T],
    /,
    *,
    row: bool = False,
) -> T:
    from telegrinder.tools.keyboard.button import BaseButton

    keyboard = button.keyboard_class().add(button)

    if row:
        keyboard = keyboard.row()

    return (
        keyboard.merge_to_last_row(keyboard_or_button)
        if not isinstance(keyboard_or_button, BaseButton)
        else keyboard.add(keyboard_or_button)
    )


def init_keyboard[T: BaseKeyboard](
    keyboard_instance: T,
    /,
    *,
    max_in_row: int = 0,
) -> T:
    for button in get_keyboard_button_rules(type(keyboard_instance)).values():
        if button.button.new_row or (max_in_row and len(keyboard_instance.keyboard[-1]) >= max_in_row):
            keyboard_instance.row()

        keyboard_instance.add(button.button)

    return keyboard_instance


class bound_keyboard_method[T: BaseKeyboard, **P, R]:  # noqa: N801
    def __init__(self, func: typing.Callable[typing.Concatenate[T, P], R], /) -> None:
        self.func = func

    def __get__(self, instance: T | None, owner: type[T]) -> typing.Callable[P, R]:
        return self.func.__get__(instance or owner.__keyboard_instance__, owner)


class RowButtons[KeyboardButton: BaseButton]:
    buttons: typing.Iterable[KeyboardButton]

    def __init__(self, *buttons: KeyboardButton, auto_row: bool = True) -> None:
        self.buttons = buttons
        self.auto_row = auto_row

    def get_data(self) -> list[dict[str, typing.Any]]:
        return [b.get_data() for b in self.buttons]


__all__ = (
    "RowButtons",
    "bound_keyboard_method",
    "copy_keyboard",
    "freaky_keyboard_merge",
    "get_keyboard_button_rules",
    "init_keyboard",
)
