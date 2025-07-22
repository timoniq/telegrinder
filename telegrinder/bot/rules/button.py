from __future__ import annotations

import typing

from telegrinder.bot.rules.abc import ABCRule, CheckResult

if typing.TYPE_CHECKING:
    from telegrinder.node.base import IsNode
    from telegrinder.tools.keyboard.button import BaseButton


class ButtonRule[KeyboardButton: BaseButton[typing.Any]](ABCRule):
    def __init__(self, button: KeyboardButton, rule: ABCRule) -> None:
        self.button = button
        self.rule = rule

    @property
    def required_nodes(self) -> dict[str, IsNode]:
        return self.rule.required_nodes

    @property
    def check(self) -> typing.Callable[..., CheckResult]:
        return self.rule.check


__all__ = ("ButtonRule",)
