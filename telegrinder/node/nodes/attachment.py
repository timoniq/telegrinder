import dataclasses
import typing

from kungfu.library.monad.option import NOTHING, Nothing, Option
from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node
from nodnod.node import Node

import telegrinder.types
from telegrinder.bot.cute_types.message import MessageCute

type AttachmentType = typing.Literal[
    "animation",
    "audio",
    "document",
    "photo",
    "poll",
    "video",
    "video_note",
    "voice",
    "successful_payment",
]

ATTACHMENT_TYPES: typing.Final[tuple[AttachmentType, ...]] = typing.get_args(AttachmentType.__value__)


@dataclasses.dataclass
class Attachment(Node):
    attachment_type: AttachmentType

    animation: Option[telegrinder.types.Animation] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    audio: Option[telegrinder.types.Audio] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    document: Option[telegrinder.types.Document] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    photo: Option[list[telegrinder.types.PhotoSize]] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    poll: Option[telegrinder.types.Poll] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    voice: Option[telegrinder.types.Voice] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    video: Option[telegrinder.types.Video] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    video_note: Option[telegrinder.types.VideoNote] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    successful_payment: Option[telegrinder.types.SuccessfulPayment] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )

    @classmethod
    def __compose__(cls, message: MessageCute) -> typing.Self:
        for attachment_type in ATTACHMENT_TYPES:
            attachment = getattr(message, attachment_type, NOTHING)

            if attachment:
                return cls(attachment_type, **{attachment_type: attachment})

        raise NodeError("No attachment found in message.")


@dataclasses.dataclass
class Photo(Node):
    sizes: list[telegrinder.types.PhotoSize]

    @classmethod
    def __compose__(cls, attachment: Attachment) -> typing.Self:
        return cls(attachment.photo.expect(NodeError("Attachment is not a photo.")))


@scalar_node
class Video:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Video:
        return attachment.video.expect(NodeError("Attachment is not a video."))


@scalar_node
class VideoNote:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.VideoNote:
        return attachment.video_note.expect(NodeError("Attachment is not a video note."))


@scalar_node
class Audio:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Audio:
        return attachment.audio.expect(NodeError("Attachment is not an audio."))


@scalar_node
class Animation:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Animation:
        return attachment.animation.expect(NodeError("Attachment is not an animation."))


@scalar_node
class Voice:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Voice:
        return attachment.voice.expect(NodeError("Attachment is not a voice."))


@scalar_node
class Document:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Document:
        return attachment.document.expect(NodeError("Attachment is not a document."))


@scalar_node
class Poll:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Poll:
        return attachment.poll.expect(NodeError("Attachment is not a poll."))


@scalar_node
class SuccessfulPayment:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.SuccessfulPayment:
        return attachment.successful_payment.expect(NodeError("Attachment is not a successful payment."))


@dataclasses.dataclass
class MediaGroup(Node):
    id: str
    items: list[MessageCute]

    @classmethod
    def __compose__(cls, message: MessageCute) -> typing.Self:
        return cls(
            id=message.media_group_id.expect(NodeError("No media group id.")),
            items=message.media_group_messages.expect(NodeError("No messages collected for media group.")),
        )


__all__ = (
    "Animation",
    "Attachment",
    "Audio",
    "Document",
    "MediaGroup",
    "Photo",
    "Poll",
    "SuccessfulPayment",
    "Video",
    "VideoNote",
    "Voice",
)
