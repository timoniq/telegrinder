from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    CHOSEN_INLINE_RESULT,
    CHOSEN_INLINE_RESULT_FOR_MESSAGE,
    CHOSEN_INLINE_RESULT_FOR_MESSAGE_FROM_USER,
    CHOSEN_INLINE_RESULT_FROM_USER,
)
from telegrinder.types.objects import ChosenInlineResult, User


class ChosenInlineResultCute(BaseCute[ChosenInlineResult], ChosenInlineResult, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    def RESULT(self, result_id: str | None = None):
        return CHOSEN_INLINE_RESULT(self.result_id if result_id is None else result_id)

    def FROM_USER(self, user_id: int | None = None):
        return CHOSEN_INLINE_RESULT_FROM_USER(self.from_user.id if user_id is None else user_id)

    def FOR_MESSAGE(self, inline_message_id: str | None = None):
        return CHOSEN_INLINE_RESULT_FOR_MESSAGE(
            inline_message_id
            if inline_message_id is not None
            else self.inline_message_id.expect(
                ValueError("Chosen inline result message hasher requires inline_message_id."),
            ),
        )

    def FOR_MESSAGE_FROM_USER(self, inline_message_id: str | None = None, user_id: int | None = None):
        return CHOSEN_INLINE_RESULT_FOR_MESSAGE_FROM_USER(
            (
                inline_message_id
                if inline_message_id is not None
                else self.inline_message_id.expect(
                    ValueError("Chosen inline result message hasher requires inline_message_id."),
                ),
                self.from_user.id if user_id is None else user_id,
            ),
        )


__all__ = ("ChosenInlineResultCute",)
