import asyncio
import contextlib
import dataclasses
import typing

from fntypes.library.monad.option import Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.cute_types.utils import MEDIA_TYPES
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.view.message import MessageView
from telegrinder.types.objects import Message, Update

WAIT_TIME: typing.Final[float] = 2.0
MAX_GROUP_PARTS: typing.Final[int] = 10


@dataclasses.dataclass(slots=True)
class MediaGroupData:
    raw_update: Update
    update_cute: UpdateCute
    messages: list[MessageCute] = dataclasses.field(default_factory=lambda: list())
    timer_task: asyncio.Task[typing.Any] | None = None
    processed: bool = False


class MediaGroupView(MessageView):
    media_groups: dict[str, MediaGroupData]

    def __init__(self, wait_time: float = WAIT_TIME) -> None:
        super().__init__()
        self.wait_time = wait_time
        self.media_groups = {}
        self._lock = asyncio.Lock()

    async def check(self, event: Update) -> bool:
        if not await super().check(event):
            return False

        if not isinstance(message := event.incoming_update, Message) or not message.media_group_id:
            return False

        return message.content_type in MEDIA_TYPES

    async def process(self, event: Update, api: API, context: Context) -> bool:
        update_cute = context.update_cute.map_or_else(
            lambda _: context.add_update_cute(event, api).update_cute.unwrap(),
            lambda update_cute: update_cute,
        )
        message_cute = update_cute.map(
            lambda update_cute: typing.cast("MessageCute", update_cute.incoming_update)
        ).unwrap()
        media_group_id = message_cute.media_group_id.unwrap()

        async with self._lock:
            if media_group_id not in self.media_groups:
                self.media_groups[media_group_id] = MediaGroupData(
                    raw_update=event, update_cute=update_cute.unwrap()
                )

            group_data = self.media_groups[media_group_id]
            if group_data.processed:
                return False

            group_data.messages.append(message_cute)

            if group_data.timer_task:
                group_data.timer_task.cancel()

            if len(group_data.messages) >= MAX_GROUP_PARTS:
                group_data.processed = True
                messages = group_data.messages.copy()
                self.media_groups.pop(media_group_id, None)
                return await self.process_media_group(
                    group_data.raw_update, group_data.update_cute, messages, api, context
                )

            group_data.timer_task = asyncio.create_task(self.wait_and_process(media_group_id, api, context))

        return True

    async def wait_and_process(self, media_group_id: str, api: API, context: Context) -> None:
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.sleep(self.wait_time)

            async with self._lock:
                if media_group_id not in self.media_groups:
                    return

                group_data = self.media_groups[media_group_id]
                if group_data.processed:
                    return

                group_data.processed = True
                messages = group_data.messages.copy()
                self.media_groups.pop(media_group_id, None)

            if messages:
                await self.process_media_group(
                    group_data.raw_update, group_data.update_cute, messages, api, context
                )

    async def process_media_group(
        self,
        initiating_event: Update,
        initiating_event_cute: UpdateCute,
        messages: list[MessageCute],
        api: API,
        context: Context,
    ) -> bool:
        if not messages:
            return False

        context.update_cute = Some(initiating_event_cute)
        message = typing.cast("MessageCute", initiating_event_cute.incoming_update)
        message.set_media_group_messages(messages)
        return await process_inner(api, initiating_event, context, self)


__all__ = ("MediaGroupView",)
