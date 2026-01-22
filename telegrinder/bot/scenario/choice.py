import typing

from telegrinder.api.api import API
from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.dispatch.waiter_machine.hasher.hasher import Hasher
from telegrinder.bot.scenario.checkbox import CallbackQueryView, Checkbox, ChoiceAction, MessageId


class Choice[Key: typing.Hashable](Checkbox[Key]):
    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = cb.data.unwrap().replace(f"{self.random_code}/", "", 1)
        if code == ChoiceAction.READY:
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
        hasher: Hasher[CallbackQueryCute, MessageId],
        view: CallbackQueryView,
        api: API,
    ) -> tuple[Key, MessageId]:
        if len(tuple(choice for choice in self.choices if choice.is_picked)) != 1:
            raise ValueError("Exactly one choice must be picked.")

        choices, m_id = await super().wait(hasher, view, api)
        return tuple(choices.keys())[tuple(choices.values()).index(True)], m_id


__all__ = ("Choice",)
