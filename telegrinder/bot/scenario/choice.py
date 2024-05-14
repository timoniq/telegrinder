import typing

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.waiter_machine import WaiterMachine

from .checkbox import Checkbox

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch.view.abc import BaseStateView


class SingleChoice(Checkbox):
    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = cb.data.unwrap().replace(self.random_code + "/", "", 1)
        if code == "ready":
            return False

        for choice in self.choices:
            choice.is_picked = False

        for i, choice in enumerate(self.choices):
            if choice.code == code:
                self.choices[i].is_picked = True
                await cb.ctx_api.edit_message_text(
                    text=self.message,
                    chat_id=cb.message.unwrap().v.chat.id,
                    message_id=cb.message.unwrap().v.message_id,
                    parse_mode=self.PARSE_MODE,
                    reply_markup=self.get_markup(),
                )

        return True

    async def wait(
        self,
        api: "API",
        view: "BaseStateView[CallbackQueryCute]",
    ) -> tuple[str, int]:
        if len(tuple(choice for choice in self.choices if choice.is_picked)) != 1:
            raise ValueError("Exactly one choice must be picked")
        choices, m_id = await super().wait(api, view)
        return tuple(choices.keys())[tuple(choices.values()).index(True)], m_id


__all__ = ("SingleChoice",)
