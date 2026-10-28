from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    REMOVED_CHAT_BOOST,
    REMOVED_CHAT_BOOST_FROM_USER,
    REMOVED_CHAT_BOOST_FROM_USER_IN_CHAT,
    REMOVED_CHAT_BOOST_IN_CHAT,
    REMOVED_CHAT_BOOST_IN_CHAT_FOR_BOOST,
    REMOVED_CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY,
)
from telegrinder.types.objects import ChatBoostRemoved


class ChatBoostRemovedCute(BaseCute[ChatBoostRemoved], ChatBoostRemoved, kw_only=True):
    def BOOST(self, boost_id: str | None = None):
        return REMOVED_CHAT_BOOST(self.boost_id if boost_id is None else boost_id)

    def IN_CHAT(self, chat_id: int | None = None):
        return REMOVED_CHAT_BOOST_IN_CHAT(self.chat.id if chat_id is None else chat_id)

    def IN_CHAT_FOR_BOOST(self, chat_id: int | None = None, boost_id: str | None = None):
        return REMOVED_CHAT_BOOST_IN_CHAT_FOR_BOOST(
            (
                self.chat.id if chat_id is None else chat_id,
                self.boost_id if boost_id is None else boost_id,
            )
        )

    def FROM_USER(self, user_id: int | None = None):
        if user_id is None:
            user_id = REMOVED_CHAT_BOOST_FROM_USER.get_data_from_event(self).expect(
                ValueError("source.user is missing.")
            )
        return REMOVED_CHAT_BOOST_FROM_USER(user_id)

    def FROM_USER_IN_CHAT(self, chat_id: int | None = None, user_id: int | None = None):
        if user_id is None:
            user_id = REMOVED_CHAT_BOOST_FROM_USER.get_data_from_event(self).expect(
                ValueError("source.user is missing.")
            )
        return REMOVED_CHAT_BOOST_FROM_USER_IN_CHAT((self.chat.id if chat_id is None else chat_id, user_id))

    def IN_CHAT_FOR_GIVEAWAY(self, chat_id: int | None = None, giveaway_message_id: int | None = None):
        if giveaway_message_id is None:
            giveaway_message_id = REMOVED_CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY.get_data_from_event(self).expect(
                ValueError("source.giveaway_message_id is missing.")
            )[1]
        return REMOVED_CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY(
            (self.chat.id if chat_id is None else chat_id, giveaway_message_id)
        )


__all__ = ("ChatBoostRemovedCute",)
