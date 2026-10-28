from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    DELETED_BUSINESS_MESSAGES,
    DELETED_BUSINESS_MESSAGES_IN_CHAT,
    DELETED_BUSINESS_MESSAGES_IN_CHAT_FOR_CONNECTION,
)
from telegrinder.types.objects import BusinessMessagesDeleted


class BusinessMessagesDeletedCute(BaseCute[BusinessMessagesDeleted], BusinessMessagesDeleted, kw_only=True):
    def CONNECTION(self, business_connection_id: str | None = None):
        return DELETED_BUSINESS_MESSAGES(
            self.business_connection_id if business_connection_id is None else business_connection_id
        )

    def IN_CHAT(self, chat_id: int | None = None):
        return DELETED_BUSINESS_MESSAGES_IN_CHAT(self.chat.id if chat_id is None else chat_id)

    def IN_CHAT_FOR_CONNECTION(self, business_connection_id: str | None = None, chat_id: int | None = None):
        return DELETED_BUSINESS_MESSAGES_IN_CHAT_FOR_CONNECTION(
            (
                self.business_connection_id if business_connection_id is None else business_connection_id,
                self.chat.id if chat_id is None else chat_id,
            )
        )


__all__ = ("BusinessMessagesDeletedCute",)
