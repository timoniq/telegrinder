import dataclasses
import typing

from fntypes import Option, Some
from fntypes.option import Nothing

import telegrinder.types

from .base import ComposeError, DataNode, ScalarNode
from .message import MessageNode


@dataclasses.dataclass
class Attachment(DataNode):
    attachment_type: typing.Literal["audio", "document", "photo", "poll", "video"]
    _: dataclasses.KW_ONLY
    audio: Option[telegrinder.types.Audio] = dataclasses.field(default_factory=lambda: Nothing())
    document: Option[telegrinder.types.Document] = dataclasses.field(
        default_factory=lambda: Nothing()
    )
    photo: Option[list[telegrinder.types.PhotoSize]] = dataclasses.field(
        default_factory=lambda: Nothing()
    )
    poll: Option[telegrinder.types.Poll] = dataclasses.field(default_factory=lambda: Nothing())
    video: Option[telegrinder.types.Video] = dataclasses.field(default_factory=lambda: Nothing())

    @classmethod
    async def compose(cls, message: MessageNode) -> "Attachment":
        for attachment_type in ("audio", "document", "photo", "poll", "video"):
            match getattr(message, attachment_type, Nothing()):
                case Some(attachment):
                    return cls(attachment_type, **{attachment_type: Some(attachment)})
        return cls.compose_error("No attachment found in message")


@dataclasses.dataclass
class Photo(DataNode):
    sizes: list[telegrinder.types.PhotoSize]

    @classmethod
    async def compose(cls, attachment: Attachment) -> typing.Self:
        if not attachment.photo:
            raise ComposeError("Attachment is not an photo")
        return cls(attachment.photo.unwrap())


class Video(ScalarNode, telegrinder.types.Video):
    @classmethod
    async def compose(cls, attachment: Attachment) -> telegrinder.types.Video:
        if not attachment.video:
            raise ComposeError("Attachment is not an video")
        return attachment.video.unwrap()


class Audio(ScalarNode, telegrinder.types.Audio):
    @classmethod
    async def compose(cls, attachment: Attachment) -> telegrinder.types.Audio:
        if not attachment.audio:
            raise ComposeError("Attachment is not an audio")
        return attachment.audio.unwrap()


class Document(ScalarNode, telegrinder.types.Document):
    @classmethod
    async def compose(cls, attachment: Attachment) -> telegrinder.types.Document:
        if not attachment.document:
            raise ComposeError("Attachment is not an document")
        return attachment.document.unwrap()


class Poll(ScalarNode, telegrinder.types.Poll):
    @classmethod
    async def compose(cls, attachment: Attachment) -> telegrinder.types.Poll:
        if not attachment.poll:
            raise ComposeError("Attachment is not an poll")
        return attachment.poll.unwrap()


__all__ = (
    "Attachment",
    "Audio",
    "Document",
    "Photo",
    "Poll",
    "Video",
)
