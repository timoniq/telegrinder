import random
import string
import typing
from dataclasses import dataclass

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.waiter_machine import WaiterMachine
from telegrinder.tools import InlineButton, InlineKeyboard
from telegrinder.types.objects import InlineKeyboardMarkup

from .abc import ABCScenario

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch import Dispatch


@dataclass
class Choice:
    name: str
    is_picked: bool
    default_text: str
    picked_text: str
    code: str


def random_code(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class Checkbox(ABCScenario):
    INVALID_CODE: str = "Invalid code"
    CALLBACK_ANSWER: str = "Done"
    PARSE_MODE: str = "MarkdownV2"

    def __init__(
        self,
        waiter_machine: WaiterMachine,
        chat_id: int,
        msg: str,
        ready_text: str = "Ready",
        max_in_row: int = 3,
    ):
        self.chat_id = chat_id
        self.msg = msg
        self.choices: list[Choice] = []
        self.ready = ready_text
        self.max_in_row = max_in_row
        self.random_code = random_code(16)
        self.waiter_machine = waiter_machine

    def get_markup(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboard(resize_keyboard=True)
        choices = self.choices.copy()
        while choices:
            while len(kb.keyboard[-1]) < self.max_in_row and choices:
                choice = choices.pop(0)
                kb.add(
                    InlineButton(
                        text=choice.default_text
                        if not choice.is_picked
                        else choice.picked_text,
                        callback_data=self.random_code + "/" + choice.code,
                    )
                )
            kb.row()
        kb.add(InlineButton(self.ready, callback_data=self.random_code + "/ready"))
        return kb.get_markup()

    def add_option(
        self, name: str, default_text: str, picked_text: str, is_picked: bool = False
    ) -> "Checkbox":
        self.choices.append(
            Choice(name, is_picked, default_text, picked_text, random_code(16))
        )
        return self

    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = cb.data.unwrap().replace(self.random_code + "/", "", 1)

        if code == "ready":
            return False

        for i, choice in enumerate(self.choices):
            if choice.code == code:
                # Toggle choice
                self.choices[i].is_picked = not self.choices[i].is_picked
                await cb.ctx_api.edit_message_text(
                    cb.message.unwrap().chat.id,
                    cb.message.unwrap().message_id,
                    text=self.msg,
                    parse_mode=self.PARSE_MODE,
                    reply_markup=self.get_markup(),
                )
                break

        return True

    async def wait(
        self, api: "API", dispatch: "Dispatch"
    ) -> tuple[dict[str, bool], int]:
        assert len(self.choices) > 1
        message = (
            await api.send_message(
                self.chat_id,
                text=self.msg,
                parse_mode=self.PARSE_MODE,
                reply_markup=self.get_markup(),
            )
        ).unwrap()
        while True:
            q: CallbackQueryCute
            q, _ = await self.waiter_machine.wait(
                dispatch.callback_query,
                (api, message.message_id),
            )
            should_continue = await self.handle(q)
            await q.answer(self.CALLBACK_ANSWER)
            if not should_continue:
                break
        return {
            choice.name: choice.is_picked for choice in self.choices
        }, message.message_id
