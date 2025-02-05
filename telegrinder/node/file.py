import typing

import telegrinder.types as tg_types
from telegrinder.api.api import API
from telegrinder.node.attachment import Animation, Audio, Document, Photo, Video, VideoNote, Voice
from telegrinder.node.base import FactoryNode

type Attachment = Animation | Audio | Document | Photo | Video | VideoNote | Voice


class _FileId(FactoryNode):
    attachment_node: type[Attachment]

    def __class_getitem__(cls, attachment_node: type[Attachment], /):
        return cls(attachment_node=attachment_node)

    @classmethod
    def get_subnodes(cls):
        return {"attach": cls.attachment_node}

    @classmethod
    def compose(cls, attach: Attachment) -> str:
        if isinstance(attach, Photo):
            return attach.sizes[-1].file_id
        return attach.file_id


class _File(FactoryNode):
    attachment_node: type[Attachment]

    def __class_getitem__(cls, attachment_node: type[Attachment], /):
        return cls(attachment_node=attachment_node)

    @classmethod
    def get_subnodes(cls):
        return {"file_id": _FileId[cls.attachment_node]}

    @classmethod
    async def compose(cls, file_id: str, api: API) -> tg_types.File:
        return (await api.get_file(file_id=file_id)).expect("File can't be downloaded.")


if typing.TYPE_CHECKING:
    type FileId[T: Attachment] = str
    type File[T: Attachment] = tg_types.File
else:
    FileId = _FileId
    File = _File


__all__ = ("File", "FileId")
