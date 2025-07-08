import asyncio
import typing
from dataclasses import dataclass, field
from typing import Dict, List

import fntypes

from telegrinder.api.api import API
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

WAIT_TIME = 2.0
MAX_GROUP_PARTS = 10


@dataclass
class MediaGroupData:
    event: Update
    messages: List[MessageCute] = field(default_factory=list)
    timer_task: asyncio.Task[None] | None = None
    processed: bool = False


class MediaGroupView(BaseView):
    def __init__(self, wait_time: float = WAIT_TIME) -> None:
        super().__init__()
        self.return_manager = MessageReturnManager()
        self.wait_time = wait_time
        self.media_groups: Dict[str, MediaGroupData] = {}
        self.lock = asyncio.Lock()

    async def check(self, event: Update) -> bool:
        if event.update_type not in (
            UpdateType.MESSAGE,
            UpdateType.BUSINESS_MESSAGE,
            UpdateType.EDITED_MESSAGE,
            UpdateType.EDITED_BUSINESS_MESSAGE,
        ):
            return False

        message = getattr(event, event.update_type.value, fntypes.Nothing()).unwrap_or(None)
        if not message:
            return False

        media_group_id = getattr(message, "media_group_id", fntypes.Nothing()).unwrap_or(None)
        if not media_group_id:
            return False

        has_media = any(
            [
                getattr(message, attr, None) and getattr(message, attr).unwrap_or(None)
                for attr in ["photo", "video", "audio", "document", "animation"]
            ]
        )

        return has_media

    async def process(self, event: Update, api: API, context: Context) -> bool:
        message = getattr(event, event.update_type.value).unwrap()
        media_group_id = message.media_group_id.unwrap()

        message_cute = MessageCute.from_update(message, bound_api=api)

        async with self.lock:
            if media_group_id not in self.media_groups:
                self.media_groups[media_group_id] = MediaGroupData(event=event)

            group_data = self.media_groups[media_group_id]

            if group_data.processed:
                return False

            group_data.messages.append(message_cute)

            if group_data.timer_task:
                group_data.timer_task.cancel()

            if len(group_data.messages) >= MAX_GROUP_PARTS:
                group_data.processed = True
                messages = group_data.messages.copy()
                del self.media_groups[media_group_id]

                await self.process_media_group(group_data.event, messages, api, context)
            else:
                group_data.timer_task = asyncio.create_task(self.wait_and_process(media_group_id, api, context))

        return True

    async def wait_and_process(self, media_group_id: str, api: API, context: Context) -> None:
        try:
            await asyncio.sleep(self.wait_time)

            async with self.lock:
                if media_group_id not in self.media_groups:
                    return

                group_data = self.media_groups[media_group_id]
                if group_data.processed:
                    return

                group_data.processed = True
                messages = group_data.messages.copy()
                event = group_data.event

                del self.media_groups[media_group_id]

            if messages:
                await self.process_media_group(event, messages, api, context)

        except asyncio.CancelledError:
            pass

    async def process_media_group(
        self, initiating_event: Update, messages: List[MessageCute], api: API, context: Context
    ) -> None:
        if not messages:
            return

        incoming_update = context.update_cute.unwrap().incoming_update
        message = typing.cast("MessageCute", incoming_update)
        message.media_group_messages = messages

        await process_inner(api, initiating_event, context, self)


__all__ = ("MediaGroupView",)
