import dataclasses
import typing

from fntypes.option import Nothing, Option, Some

import telegrinder.types
from telegrinder.node.base import ComposeError, DataNode, ScalarNode
from telegrinder.node.message import MessageNode


@dataclasses.dataclass(slots=True)
class Attachment(DataNode):
    attachment_type: typing.Literal["audio", "document", "photo", "poll", "video", "successful_payment"]

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
    video: Option[telegrinder.types.Video] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    successful_payment: Option[telegrinder.types.SuccessfulPayment] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )

    @classmethod
    def get_attachment_types(cls) -> tuple[typing.Any, ...]:
        return typing.get_args(cls.__annotations__["attachment_type"])

    @classmethod
    def compose(cls, message: MessageNode) -> "Attachment":
        for attachment_type in cls.get_attachment_types():
            match getattr(message, attachment_type, Nothing()):
                case Some(attachment):
                    return cls(attachment_type, **{attachment_type: Some(attachment)})
        return cls.compose_error("No attachment found in message.")


@dataclasses.dataclass(slots=True)
class Photo(DataNode):
    sizes: list[telegrinder.types.PhotoSize]

    @classmethod
    def compose(cls, attachment: Attachment) -> typing.Self:
        if not attachment.photo:
            raise ComposeError("Attachment is not a photo.")
        return cls(attachment.photo.unwrap())


class Video(ScalarNode, telegrinder.types.Video):
    @classmethod
    def compose(cls, attachment: Attachment) -> telegrinder.types.Video:
        if not attachment.video:
            raise ComposeError("Attachment is not a video.")
        return attachment.video.unwrap()


class Audio(ScalarNode, telegrinder.types.Audio):
    @classmethod
    def compose(cls, attachment: Attachment) -> telegrinder.types.Audio:
        if not attachment.audio:
            raise ComposeError("Attachment is not an audio.")
        return attachment.audio.unwrap()


class Document(ScalarNode, telegrinder.types.Document):
    @classmethod
    def compose(cls, attachment: Attachment) -> telegrinder.types.Document:
        if not attachment.document:
            raise ComposeError("Attachment is not a document.")
        return attachment.document.unwrap()


class Poll(ScalarNode, telegrinder.types.Poll):
    @classmethod
    def compose(cls, attachment: Attachment) -> telegrinder.types.Poll:
        if not attachment.poll:
            raise ComposeError("Attachment is not a poll.")
        return attachment.poll.unwrap()


class SuccessfulPayment(ScalarNode, telegrinder.types.SuccessfulPayment):
    @classmethod
    def compose(cls, attachment: Attachment) -> telegrinder.types.SuccessfulPayment:
        if not attachment.successful_payment:
            raise ComposeError("Attachment is not a successful payment.")
        return attachment.successful_payment.unwrap()


__all__ = (
    "Attachment",
    "Audio",
    "Document",
    "Photo",
    "Poll",
    "SuccessfulPayment",
    "Video",
)
