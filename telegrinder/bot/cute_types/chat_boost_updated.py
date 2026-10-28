from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    CHAT_BOOST,
    CHAT_BOOST_FROM_USER,
    CHAT_BOOST_FROM_USER_IN_CHAT,
    CHAT_BOOST_IN_CHAT,
    CHAT_BOOST_IN_CHAT_FOR_BOOST,
    CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY,
)
from telegrinder.types.objects import ChatBoostUpdated


class ChatBoostUpdatedCute(BaseCute[ChatBoostUpdated], ChatBoostUpdated, kw_only=True):
    def BOOST(self, boost_id: str | None = None):
        return CHAT_BOOST(
            boost_id if boost_id is not None else self.boost.boost_id,
        )

    def IN_CHAT(self, chat_id: int | None = None):
        return CHAT_BOOST_IN_CHAT(
            chat_id if chat_id is not None else self.chat.id,
        )

    def IN_CHAT_FOR_BOOST(self, chat_id: int | None = None, boost_id: str | None = None):
        return CHAT_BOOST_IN_CHAT_FOR_BOOST(
            (
                chat_id if chat_id is not None else self.chat.id,
                boost_id if boost_id is not None else self.boost.boost_id,
            ),
        )

    def FROM_USER(self, user_id: int | None = None):
        return CHAT_BOOST_FROM_USER(
            user_id
            if user_id is not None
            else CHAT_BOOST_FROM_USER.get_data_from_event(self).expect(
                ValueError("CHAT_BOOST_FROM_USER requires user_id.")
            ),
        )

    def FROM_USER_IN_CHAT(self, chat_id: int | None = None, user_id: int | None = None):
        return CHAT_BOOST_FROM_USER_IN_CHAT(
            (
                chat_id if chat_id is not None else self.chat.id,
                user_id
                if user_id is not None
                else CHAT_BOOST_FROM_USER.get_data_from_event(self).expect(
                    ValueError("CHAT_BOOST_FROM_USER_IN_CHAT requires user_id.")
                ),
            ),
        )

    def IN_CHAT_FOR_GIVEAWAY(self, chat_id: int | None = None, giveaway_message_id: int | None = None):
        return CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY(
            (
                chat_id if chat_id is not None else self.chat.id,
                giveaway_message_id
                if giveaway_message_id is not None
                else CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY.get_data_from_event(self).expect(
                    ValueError("CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY requires giveaway_message_id.")
                )[1],
            ),
        )


__all__ = ("ChatBoostUpdatedCute",)
