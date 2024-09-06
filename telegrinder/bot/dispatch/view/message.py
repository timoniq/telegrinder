import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseStateView
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

MessageUpdateType: typing.TypeAlias = typing.Literal[
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
]


class MessageView(BaseStateView[MessageCute]):
    def __init__(self, *, update_type: MessageUpdateType | None = None) -> None:
        self.auto_rules = []
        self.handlers = []
        self.update_type = update_type
        self.middlewares = []
        self.return_manager = MessageReturnManager()

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(
            self.__class__.__name__,
            "any message update" if self.update_type is None else self.update_type.value,
        )

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat_id

    async def check(self, event: Update) -> bool:
        return not (
            self.update_type is not None
            and self.update_type != event.update_type
            or not await super().check(event)
        )


__all__ = ("MessageView",)
