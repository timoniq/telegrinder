import typing

from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

type MessageUpdateType = typing.Literal[
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
]

MESSAGE_UPDATE_TYPES: typing.Final[tuple[MessageUpdateType, ...]] = (
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
)


class MessageView(BaseView):
    def __init__(self, update_type: MessageUpdateType | None = None) -> None:
        super().__init__(update_type)
        self.return_manager = MessageReturnManager()

    async def check(self, event: Update) -> bool:
        return (
            event.update_type in MESSAGE_UPDATE_TYPES if self.update_type is None else await super().check(event)
        )


__all__ = ("MessageView",)
