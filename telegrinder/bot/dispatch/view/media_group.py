from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import typing

from fntypes.library import Error, Ok, Result
from fntypes.library.monad.option import Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.view.base import EventModelView
from telegrinder.bot.rules.media import IsMediaGroup
from telegrinder.types.objects import Message, Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager

WAIT_TIME: typing.Final = 2.0
MAX_GROUP_PARTS: typing.Final = 10


@dataclasses.dataclass(slots=True)
class MediaGroupData:
    raw_update: Update
    update_cute: UpdateCute
    messages: list[MessageCute] = dataclasses.field(default_factory=lambda: list())
    timer_task: asyncio.Task[typing.Any] | None = None
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
        self._lock = asyncio.Lock()

    async def process(self, event: Update, api: API, context: Context) -> Result[str, str]:
        update_cute = context.update_cute.map_or_else(
            lambda _: context.add_update_cute(event, api).update_cute.unwrap(),
            lambda update_cute: update_cute,
        )
        message_cute = update_cute.map(
            lambda update_cute: typing.cast("MessageCute", update_cute.incoming_update),
        ).unwrap()
        media_group_id = message_cute.media_group_id.unwrap()

        async with self._lock:
            if media_group_id not in self.media_groups:
                self.media_groups[media_group_id] = MediaGroupData(raw_update=event, update_cute=update_cute.unwrap())

            group_data = self.media_groups[media_group_id]
            if group_data.processed:
                return Error("Media group already processed.")

            group_data.messages.append(message_cute)

            if group_data.timer_task:
                group_data.timer_task.cancel()

            if len(group_data.messages) >= MAX_GROUP_PARTS:
                group_data.processed = True
                messages = group_data.messages.copy()
                self.media_groups.pop(media_group_id, None)
                return await self.process_media_group(
                    group_data.raw_update,
                    group_data.update_cute,
                    messages,
                    api,
                    context,
                )

            group_data.timer_task = asyncio.create_task(self.wait_and_process(media_group_id, api, context))

        return Ok("Media group processed.")

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
                    group_data.raw_update,
                    group_data.update_cute,
                    messages,
                    api,
                    context,
                )

    async def process_media_group(
        self,
        initiating_event: Update,
        initiating_event_cute: UpdateCute,
        messages: list[MessageCute],
        api: API,
        context: Context,
    ) -> Result[str, str]:
        if not messages:
            return Error("No messages in media group.")

        context.update_cute = Some(initiating_event_cute)
        message = typing.cast("MessageCute", initiating_event_cute.incoming_update)
        message.media_group_messages = Some(messages)
        return await process_inner(api, initiating_event, context, self)


__all__ = ("MediaGroupView",)
