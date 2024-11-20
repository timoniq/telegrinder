import dataclasses
import enum
import secrets
import typing

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.dispatch.waiter_machine.hasher.hasher import Hasher
from telegrinder.bot.dispatch.waiter_machine.machine import WaiterMachine
from telegrinder.bot.scenario.abc import ABCScenario
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.tools.parse_mode import ParseMode
from telegrinder.types.objects import InlineKeyboardMarkup

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.dispatch.view.base import BaseStateView


class ChoiceAction(enum.StrEnum):
    READY = "ready"
    CANCEL = "cancel"


@dataclasses.dataclass(slots=True)
class Choice[Key: typing.Hashable]:
    key: Key
    is_picked: bool
    default_text: str
    picked_text: str
    code: str


class _Checkbox(ABCScenario[CallbackQueryCute]):
    INVALID_CODE = "Invalid code"
    CALLBACK_ANSWER = "Done"
    PARSE_MODE = ParseMode.HTML

    def __init__(
        self,
        waiter_machine: WaiterMachine,
        chat_id: int,
        message: str,
        *,
        ready_text: str = "Ready",
        cancel_text: str | None = None,
        max_in_row: int = 3,
    ) -> None:
        self.chat_id = chat_id
        self.message = message
        self.choices: list[Choice[typing.Hashable]] = []
        self.ready = ready_text
        self.max_in_row = max_in_row
        self.random_code = secrets.token_hex(8)
        self.waiter_machine = waiter_machine
        self.cancel_text = cancel_text

    def __repr__(self) -> str:
        return (
            "<{}@{!r}: (choices={!r}, max_in_row={}) with waiter_machine={!r}, ready_text={!r} "
            "for chat_id={} with message={!r}>"
        ).format(
            self.__class__.__name__,
            self.random_code,
            self.choices,
            self.max_in_row,
            self.waiter_machine,
            self.ready,
            self.chat_id,
            self.message,
        )

    def get_markup(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboard()
        choices = self.choices.copy()
        while choices:
            while len(kb.keyboard[-1]) < self.max_in_row and choices:
                choice = choices.pop(0)
                kb.add(
                    InlineButton(
                        text=(choice.default_text if not choice.is_picked else choice.picked_text),
                        callback_data=self.random_code + "/" + choice.code,
                    )
                )
            kb.row()

        kb.add(InlineButton(self.ready, callback_data=self.random_code + "/" + ChoiceAction.READY))
        if self.cancel_text is not None:
            kb.row()
            kb.add(InlineButton(self.cancel_text, callback_data=self.random_code + "/" + ChoiceAction.CANCEL))

        return kb.get_markup()

    def add_option[Key: typing.Hashable](
        self,
        key: Key,
        default_text: str,
        picked_text: str,
        *,
        is_picked: bool = False,
    ) -> "Checkbox[Key]":
        self.choices.append(
            Choice(key, is_picked, default_text, picked_text, secrets.token_hex(8)),
        )
        return self  # type: ignore

    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = cb.data.unwrap().replace(self.random_code + "/", "", 1)

        match code:
            case ChoiceAction.READY:
                return False
            case ChoiceAction.CANCEL:
                self.choices = []
                return False

        for i, choice in enumerate(self.choices):
            if choice.code == code:
                # Toggle choice
                self.choices[i].is_picked = not self.choices[i].is_picked
                await cb.edit_text(
                    text=self.message,
                    parse_mode=self.PARSE_MODE,
                    reply_markup=self.get_markup(),
                )
                break

        return True

    async def wait(
        self,
        hasher: Hasher[CallbackQueryCute, int],
        api: "API",
    ) -> tuple[dict[typing.Hashable, bool], int]:
        assert len(self.choices) > 0
        message = (
            await api.send_message(
                chat_id=self.chat_id,
                text=self.message,
                parse_mode=self.PARSE_MODE,
                reply_markup=self.get_markup(),
            )
        ).unwrap()

        while True:
            q, _ = await self.waiter_machine.wait(
                hasher,
                data=message.message_id,
            )
            should_continue = await self.handle(q)
            await q.answer(self.CALLBACK_ANSWER)
            if not should_continue:
                break

        return (
            {choice.key: choice.is_picked for choice in self.choices},
            message.message_id,
        )


if typing.TYPE_CHECKING:

    class Checkbox[Key: typing.Hashable](_Checkbox):
        choices: list[Choice[Key]]

        async def wait(
            self,
            hasher: Hasher[CallbackQueryCute, int],
            api: "API",
        ) -> tuple[dict[Key, bool], int]: ...

else:
    Checkbox = _Checkbox


__all__ = ("Checkbox", "Choice")
