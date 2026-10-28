from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    POLL_ANSWER,
    POLL_ANSWER_FROM_CHAT,
    POLL_ANSWER_FROM_USER,
    POLL_ANSWER_IN_POLL_FROM_CHAT,
    POLL_ANSWER_IN_POLL_FROM_USER,
)
from telegrinder.types.objects import PollAnswer


class PollAnswerCute(BaseCute[PollAnswer], PollAnswer, kw_only=True):
    def POLL(self, poll_id: str | None = None):
        return POLL_ANSWER(
            poll_id if poll_id is not None else self.poll_id,
        )

    def FROM_USER(self, user_id: int | None = None):
        return POLL_ANSWER_FROM_USER(
            user_id
            if user_id is not None
            else self.user.map(lambda user: user.id).expect(ValueError("POLL_ANSWER_FROM_USER requires user_id.")),
        )

    def IN_POLL_FROM_USER(self, poll_id: str | None = None, user_id: int | None = None):
        return POLL_ANSWER_IN_POLL_FROM_USER(
            (
                poll_id if poll_id is not None else self.poll_id,
                user_id
                if user_id is not None
                else self.user.map(lambda user: user.id).expect(
                    ValueError("POLL_ANSWER_IN_POLL_FROM_USER requires user_id.")
                ),
            ),
        )

    def FROM_CHAT(self, chat_id: int | None = None):
        return POLL_ANSWER_FROM_CHAT(
            chat_id
            if chat_id is not None
            else self.voter_chat.map(lambda chat: chat.id).expect(
                ValueError("POLL_ANSWER_FROM_CHAT requires chat_id.")
            ),
        )

    def IN_POLL_FROM_CHAT(self, poll_id: str | None = None, chat_id: int | None = None):
        return POLL_ANSWER_IN_POLL_FROM_CHAT(
            (
                poll_id if poll_id is not None else self.poll_id,
                chat_id
                if chat_id is not None
                else self.voter_chat.map(lambda chat: chat.id).expect(
                    ValueError("POLL_ANSWER_IN_POLL_FROM_CHAT requires chat_id.")
                ),
            ),
        )


__all__ = ("PollAnswerCute",)
