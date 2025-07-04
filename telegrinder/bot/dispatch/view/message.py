import typing

from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType

type MessageUpdateType = typing.Literal[
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
]


class MessageView(BaseView):
    def __init__(self, update_type: MessageUpdateType) -> None:
        super().__init__(update_type)
        self.return_manager = MessageReturnManager()


__all__ = ("MessageView",)
