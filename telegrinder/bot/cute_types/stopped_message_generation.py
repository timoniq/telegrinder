from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    MESSAGE_GENERATION_STOPPED,
    MESSAGE_GENERATION_STOPPED_IN_CHAT,
    MESSAGE_GENERATION_STOPPED_IN_CHAT_FOR_DRAFT,
    MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD,
    MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD_FOR_DRAFT,
)
from telegrinder.types.objects import MessageGenerationStopped


class MessageGenerationStoppedCute(BaseCute[MessageGenerationStopped], MessageGenerationStopped, kw_only=True):
    def DRAFT(self, draft_id: int | None = None):
        return MESSAGE_GENERATION_STOPPED(self.draft_id if draft_id is None else draft_id)

    def IN_CHAT(self, chat_id: int | None = None):
        return MESSAGE_GENERATION_STOPPED_IN_CHAT(self.chat.id if chat_id is None else chat_id)

    def IN_CHAT_FOR_DRAFT(self, chat_id: int | None = None, draft_id: int | None = None):
        return MESSAGE_GENERATION_STOPPED_IN_CHAT_FOR_DRAFT(
            (
                self.chat.id if chat_id is None else chat_id,
                self.draft_id if draft_id is None else draft_id,
            ),
        )

    def IN_CHAT_THREAD(self, message_thread_id: int | None = None, chat_id: int | None = None):
        return MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD(
            (
                self.message_thread_id.expect(
                    ValueError("Stopped message generation hasher requires message_thread_id."),
                )
                if message_thread_id is None
                else message_thread_id,
                self.chat.id if chat_id is None else chat_id,
            ),
        )

    def IN_CHAT_THREAD_FOR_DRAFT(
        self,
        draft_id: int | None = None,
        message_thread_id: int | None = None,
        chat_id: int | None = None,
    ):
        return MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD_FOR_DRAFT(
            (
                self.draft_id if draft_id is None else draft_id,
                self.message_thread_id.expect(
                    ValueError("Stopped message generation hasher requires message_thread_id."),
                )
                if message_thread_id is None
                else message_thread_id,
                self.chat.id if chat_id is None else chat_id,
            ),
        )


__all__ = ("MessageGenerationStoppedCute",)
