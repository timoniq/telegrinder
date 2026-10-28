from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    MESSAGE_REACTION_FROM_ACTOR_CHAT,
    MESSAGE_REACTION_FROM_USER,
    MESSAGE_REACTION_FROM_USER_IN_CHAT,
    MESSAGE_REACTION_IN_CHAT,
    MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE,
    MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_ACTOR_CHAT,
    MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_USER,
)
from telegrinder.types.objects import MessageReactionUpdated


class MessageReactionUpdatedCute(BaseCute[MessageReactionUpdated], MessageReactionUpdated, kw_only=True):
    def IN_CHAT(self, chat_id: int | None = None):
        return MESSAGE_REACTION_IN_CHAT(self.chat.id if chat_id is None else chat_id)

    def IN_CHAT_FOR_MESSAGE(self, chat_id: int | None = None, message_id: int | None = None):
        return MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE(
            (
                self.chat.id if chat_id is None else chat_id,
                self.message_id if message_id is None else message_id,
            ),
        )

    def FROM_USER(self, user_id: int | None = None):
        return MESSAGE_REACTION_FROM_USER(
            self.user.expect(ValueError("Message reaction hasher requires user.")).id if user_id is None else user_id,
        )

    def FROM_USER_IN_CHAT(self, chat_id: int | None = None, user_id: int | None = None):
        return MESSAGE_REACTION_FROM_USER_IN_CHAT(
            (
                self.chat.id if chat_id is None else chat_id,
                self.user.expect(ValueError("Message reaction hasher requires user.")).id
                if user_id is None
                else user_id,
            ),
        )

    def IN_CHAT_FOR_MESSAGE_FROM_USER(
        self,
        chat_id: int | None = None,
        message_id: int | None = None,
        user_id: int | None = None,
    ):
        return MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_USER(
            (
                self.chat.id if chat_id is None else chat_id,
                self.message_id if message_id is None else message_id,
                self.user.expect(ValueError("Message reaction hasher requires user.")).id
                if user_id is None
                else user_id,
            ),
        )

    def FROM_ACTOR_CHAT(self, actor_chat_id: int | None = None):
        return MESSAGE_REACTION_FROM_ACTOR_CHAT(
            self.actor_chat.expect(ValueError("Message reaction hasher requires actor_chat.")).id
            if actor_chat_id is None
            else actor_chat_id,
        )

    def IN_CHAT_FOR_MESSAGE_FROM_ACTOR_CHAT(
        self,
        chat_id: int | None = None,
        message_id: int | None = None,
        actor_chat_id: int | None = None,
    ):
        return MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_ACTOR_CHAT(
            (
                self.chat.id if chat_id is None else chat_id,
                self.message_id if message_id is None else message_id,
                self.actor_chat.expect(ValueError("Message reaction hasher requires actor_chat.")).id
                if actor_chat_id is None
                else actor_chat_id,
            ),
        )


__all__ = ("MessageReactionUpdatedCute",)
