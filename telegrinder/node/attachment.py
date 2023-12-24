import typing
from dataclasses import dataclass

import telegrinder.types

from .base import DataNode, ScalarNode
from .message import MessageNode


@dataclass
class Attachment(DataNode):

    attachment_type: typing.Literal["photo", "video", "audio", "document"]

    photo: list[telegrinder.types.PhotoSize] | None = None
    video: telegrinder.types.Video | None = None
    audio: telegrinder.types.Audio | None = None
    document: telegrinder.types.Document | None = None

    @classmethod
    async def compose(cls, message: MessageNode) -> "Attachment":
        for attachment_type in ("photo", "video", "audio", "document"):
            if attachment := getattr(message, attachment_type):
                return cls(attachment_type, **{attachment_type: attachment.unwrap()})
        return cls.compose_error("No attachment found in message")


@dataclass
class Photo(DataNode):
    sizes: list[telegrinder.types.PhotoSize]

    @classmethod
    async def compose(cls, attachment: Attachment) -> "Photo":
        if not attachment.photo:
            cls.compose_error("Attachment is not a photo")
        return cls(attachment.photo)


class Video(ScalarNode, telegrinder.types.Video):
    @classmethod
    async def compose(cls, attachment: Attachment) -> "telegrinder.types.Video":
        if not attachment.video:
            return cls.compose_error("Attachment is not a video")
        return attachment.video


class Audio(ScalarNode, telegrinder.types.Audio):
    @classmethod
    async def compose(cls, attachment: Attachment) -> "telegrinder.types.Audio":
        if not attachment.audio:
            return cls.compose_error("Attachment is not an audio")
        return attachment.audio
