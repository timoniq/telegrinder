from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    MESSAGE_REACTION_COUNT_IN_CHAT,
    MESSAGE_REACTION_COUNT_IN_CHAT_FOR_MESSAGE,
)
from telegrinder.types.objects import MessageReactionCountUpdated


class MessageReactionCountUpdatedCute(BaseCute[MessageReactionCountUpdated], MessageReactionCountUpdated, kw_only=True):
    def IN_CHAT(self, chat_id: int | None = None):
        return MESSAGE_REACTION_COUNT_IN_CHAT(self.chat.id if chat_id is None else chat_id)

    def IN_CHAT_FOR_MESSAGE(self, chat_id: int | None = None, message_id: int | None = None):
        return MESSAGE_REACTION_COUNT_IN_CHAT_FOR_MESSAGE(
            (
                self.chat.id if chat_id is None else chat_id,
                self.message_id if message_id is None else message_id,
            ),
        )


__all__ = ("MessageReactionCountUpdatedCute",)
