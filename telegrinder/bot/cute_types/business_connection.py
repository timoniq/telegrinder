from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    BUSINESS_CONNECTION,
    BUSINESS_CONNECTION_FROM_USER,
    BUSINESS_CONNECTION_FROM_USER_IN_USER_CHAT,
    BUSINESS_CONNECTION_IN_USER_CHAT,
)
from telegrinder.types.objects import BusinessConnection


class BusinessConnectionCute(BaseCute[BusinessConnection], BusinessConnection, kw_only=True):
    def CONNECTION(self, business_connection_id: str | None = None):
        return BUSINESS_CONNECTION(self.id if business_connection_id is None else business_connection_id)

    def FROM_USER(self, user_id: int | None = None):
        return BUSINESS_CONNECTION_FROM_USER(self.user.id if user_id is None else user_id)

    def IN_USER_CHAT(self, user_chat_id: int | None = None):
        return BUSINESS_CONNECTION_IN_USER_CHAT(self.user_chat_id if user_chat_id is None else user_chat_id)

    def FROM_USER_IN_USER_CHAT(self, user_chat_id: int | None = None, user_id: int | None = None):
        return BUSINESS_CONNECTION_FROM_USER_IN_USER_CHAT(
            (
                self.user_chat_id if user_chat_id is None else user_chat_id,
                self.user.id if user_id is None else user_id,
            )
        )


__all__ = ("BusinessConnectionCute",)
