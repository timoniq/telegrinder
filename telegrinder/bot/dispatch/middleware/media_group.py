import asyncio
import dataclasses
import typing

from kungfu.library.monad.option import Some

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware

type MediaGroupId = str

WAIT_TIME: typing.Final = 2.0
MAX_GROUP_PARTS: typing.Final = 10


@dataclasses.dataclass(frozen=True, slots=True)
class MediaGroupData:
    event: asyncio.Event
    timer: asyncio.TimerHandle
    messages: list[MessageCute] = dataclasses.field(default_factory=list)


class MediaGroupMiddleware(ABCMiddleware):
    media_groups: dict[MediaGroupId, MediaGroupData]

    def __init__(self, *, wait_time: float = WAIT_TIME) -> None:
        self.wait_time = wait_time
        self.media_groups = {}

    def __bool__(self) -> bool:
        return bool(self.media_groups)

    async def pre(self, message: MessageCute | None, context: Context) -> bool:
        if message is None:
            return True

        media_group_id = message.media_group_id.unwrap_or_none()

        if not media_group_id:
            return True

        if media_group_id not in self.media_groups:
            media_group_data = MediaGroupData(
                event=(event := asyncio.Event()),
                timer=asyncio.get_running_loop().call_later(self.wait_time, event.set),
                messages=[message],
            )
            self.media_groups[media_group_id] = media_group_data

            await event.wait()

            message.media_group_messages = Some(media_group_data.messages)
            self.media_groups.pop(media_group_id, None)
            return True

        media_group_data = self.media_groups[media_group_id]
        media_group_data.messages.append(message)

        if len(media_group_data.messages) >= MAX_GROUP_PARTS:
            if not media_group_data.timer.cancelled():
                media_group_data.timer.cancel()

            if not media_group_data.event.is_set():
                media_group_data.event.set()

            self.media_groups.pop(media_group_id, None)

        return False


__all__ = ("MediaGroupMiddleware",)
