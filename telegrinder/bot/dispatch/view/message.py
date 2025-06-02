import typing

from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Message, Update

MessageUpdateType: typing.TypeAlias = typing.Literal[
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
]


class MessageView(BaseView):
    def __init__(self, *, update_type: MessageUpdateType | None = None) -> None:
        super().__init__(update_type)
        self.return_manager = MessageReturnManager()

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(
            type(self).__name__,
            "any message update" if self.update_type is None else self.update_type.value,
        )

    async def check(self, event: Update) -> bool:
        return (
            await super().check(event)
            if self.update_type is not None
            else isinstance(event.incoming_update, Message)
        )


__all__ = ("MessageView",)
