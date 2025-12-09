import dataclasses
import typing

from kungfu.library.monad.option import Nothing, Option, Some
from nodnod.error import NodeError
from nodnod.interface.data import DataNode
from nodnod.interface.scalar import scalar_node

import telegrinder.types
from telegrinder.bot.cute_types.message import MessageCute

type AttachmentType = typing.Literal[
    "audio",
    "animation",
    "document",
    "photo",
    "poll",
    "voice",
    "video",
    "video_note",
    "successful_payment",
]


@dataclasses.dataclass(slots=True)
class Attachment(DataNode):
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
    poll: Option[telegrinder.types.Poll] = dataclasses.field(default_factory=lambda: Nothing(), kw_only=True)
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
    def get_attachment_types(cls) -> tuple[AttachmentType, ...]:
        return typing.get_args(AttachmentType.__value__)

    @classmethod
    def __compose__(cls, message: MessageCute) -> typing.Self:
        for attachment_type in cls.get_attachment_types():
            match getattr(message, attachment_type, Nothing()):
                case Some(attachment):
                    return cls(attachment_type, **{attachment_type: Some(attachment)})

        raise NodeError("No attachment found in message.")


@dataclasses.dataclass(slots=True)
class Photo(DataNode):
    sizes: list[telegrinder.types.PhotoSize]

    @classmethod
    def __compose__(cls, attachment: Attachment) -> typing.Self:
        if not attachment.photo:
            raise NodeError("Attachment is not a photo.")
        return cls(attachment.photo.unwrap())


@scalar_node
class Video:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Video:
        if not attachment.video:
            raise NodeError("Attachment is not a video.")
        return attachment.video.unwrap()


@scalar_node
class VideoNote:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.VideoNote:
        if not attachment.video_note:
            raise NodeError("Attachment is not a video note.")
        return attachment.video_note.unwrap()


@scalar_node
class Audio:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Audio:
        if not attachment.audio:
            raise NodeError("Attachment is not an audio.")
        return attachment.audio.unwrap()


@scalar_node
class Animation:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Animation:
        if not attachment.animation:
            raise NodeError("Attachment is not an animation.")
        return attachment.animation.unwrap()


@scalar_node
class Voice:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Voice:
        if not attachment.voice:
            raise NodeError("Attachment is not a voice.")
        return attachment.voice.unwrap()


@scalar_node
class Document:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Document:
        if not attachment.document:
            raise NodeError("Attachment is not a document.")
        return attachment.document.unwrap()


@scalar_node
class Poll:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.Poll:
        if not attachment.poll:
            raise NodeError("Attachment is not a poll.")
        return attachment.poll.unwrap()


@scalar_node
class SuccessfulPayment:
    @classmethod
    def __compose__(cls, attachment: Attachment) -> telegrinder.types.SuccessfulPayment:
        if not attachment.successful_payment:
            raise NodeError("Attachment is not a successful payment.")
        return attachment.successful_payment.unwrap()


@dataclasses.dataclass(slots=True)
class MediaGroup(DataNode):
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
