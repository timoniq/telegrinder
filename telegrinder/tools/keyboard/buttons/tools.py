import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.buttons.base import BaseButton


class RowButtons[KeyboardButton: BaseButton]:
    buttons: typing.Iterable[KeyboardButton]

    def __init__(self, *buttons: KeyboardButton, auto_row: bool = True) -> None:
        self.buttons = buttons
        self.auto_row = auto_row

    def get_data(self) -> list[dict[str, typing.Any]]:
        return [b.get_data() for b in self.buttons]


__all__ = ("RowButtons",)
