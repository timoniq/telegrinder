import typing

from telegrinder.bot.rules.abc import ABCRule, CheckResult

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.button import BaseButton


class ButtonRule[KeyboardButton: BaseButton[typing.Any]](ABCRule):
    def __init__(self, button: KeyboardButton, rule: ABCRule) -> None:
        self.button = button
        self.rule = rule
        self.composable = rule.composable

    @property
    def check(self) -> typing.Callable[..., CheckResult]:
        return self.rule.check


__all__ = ("ButtonRule",)
