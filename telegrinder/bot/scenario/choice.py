import typing

from telegrinder.bot.cute_types import CallbackQueryCute

from .checkbox import Checkbox

if typing.TYPE_CHECKING:
    from telegrinder.api import API
    from telegrinder.bot.dispatch.view.abc import ABCStateView


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
                    chat_id=cb.message.unwrap().chat.id,
                    message_id=cb.message.unwrap().message_id,
                    text=self.msg,
                    parse_mode=self.PARSE_MODE,
                    reply_markup=self.get_markup(),
                )

        return True

    async def wait(
        self,
        api: "API",
        cb_view: "ABCStateView[CallbackQueryCute]",
    ) -> tuple[str, int]:
        if len([choice for choice in self.choices if choice.is_picked]) != 1:
            raise ValueError("Exactly one choice must be picked")
        choices, m_id = await super().wait(api, cb_view)
        return list(choices.keys())[list(choices.values()).index(True)], m_id


__all__ = ("SingleChoice",)
