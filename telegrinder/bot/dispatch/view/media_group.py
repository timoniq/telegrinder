import asyncio
import dataclasses
import typing

from kungfu.library import Error, Ok, Result
from kungfu.library.monad.option import Some

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.view.base import EventModelView
from telegrinder.bot.rules.media import IsMediaGroup
from telegrinder.types.objects import Message, Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message import MessageCute
    from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager

WAIT_TIME: typing.Final = 2.0
MAX_GROUP_PARTS: typing.Final = 10


@dataclasses.dataclass(slots=True)
class MediaGroupData:
    event: asyncio.Event
    timer: asyncio.TimerHandle
    messages: list[MessageCute] = dataclasses.field(default_factory=lambda: list())
    processed: bool = False


class MediaGroupView(EventModelView[Message]):
    media_groups: dict[str, MediaGroupData]

    def __init__(
        self,
        *,
        wait_time: float = WAIT_TIME,
        return_manager: ABCReturnManager | None = None,
    ) -> None:
        super().__init__(model=Message, return_manager=return_manager)

        self.filter = IsMediaGroup()
        self.wait_time = wait_time
        self.media_groups = {}

    async def process(self, api: API, update: Update, context: Context) -> Result[str, str]:
        message_cute = typing.cast("MessageCute", context.update_cute.unwrap().incoming_update)
        media_group_id = message_cute.media_group_id.unwrap()

        if media_group_id not in self.media_groups:
            loop = asyncio.get_running_loop()
            event = asyncio.Event()
            media_group_data = MediaGroupData(
                event=event,
                timer=loop.call_later(self.wait_time, event.set),
                messages=[message_cute],
            )
            self.media_groups[media_group_id] = media_group_data

            await event.wait()

            media_group_data.processed = True
            self.media_groups.pop(media_group_id, None)
            return await self.process_media_group(update, api, context, media_group_data.messages)

        group_data = self.media_groups[media_group_id]

        if group_data.processed:
            self.media_groups.pop(media_group_id, None)
            return Error("Media group already processed.")

        group_data.messages.append(message_cute)

        if len(group_data.messages) >= MAX_GROUP_PARTS:
            if not group_data.timer.cancelled():
                group_data.timer.cancel()

            if not group_data.event.is_set():
                group_data.event.set()

            self.media_groups.pop(media_group_id, None)

        return Ok("Media group processed.")

    async def process_media_group(
        self,
        update: Update,
        api: API,
        context: Context,
        messages: list[MessageCute],
    ) -> Result[str, str]:
        if not messages:
            return Error("No messages in media group.")

        message = typing.cast("MessageCute", context.update_cute.unwrap().incoming_update)
        message.media_group_messages = Some(messages)
        return await process_inner(api, update, context, self)


__all__ = ("MediaGroupView",)
