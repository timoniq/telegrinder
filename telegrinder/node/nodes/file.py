import typing

from nodnod.error import NodeError
from nodnod.interface.node_constructor import NodeConstructor

import telegrinder.types as tg_types
from telegrinder.api.api import API
from telegrinder.node.nodes.attachment import Animation, Audio, Document, Photo, Video, VideoNote, Voice

type Attachment = Animation | Audio | Document | Photo | Video | VideoNote | Voice


class FileIdNode(NodeConstructor):
    def __init__(self, attachment_node: type[Attachment], /) -> None:
        self.__map__ = {Attachment: attachment_node}

    def __compose__(self, attach: Attachment) -> str:
        if isinstance(attach, Photo):
            return attach.sizes[-1].file_id
        return attach.file_id


class FileNode(NodeConstructor):
    def __init__(self, attachment_node: type[Attachment], /) -> None:
        self.__map__ = {str: FileIdNode[attachment_node]}

    async def __compose__(self, api: API, file_id: str) -> tg_types.File:
        return (await api.get_file(file_id=file_id)).expect(NodeError("File can't be downloaded."))


if typing.TYPE_CHECKING:
    type FileId[T: Attachment] = str
    type File[T: Attachment] = tg_types.File
else:
    FileId = FileIdNode
    File = FileNode


__all__ = ("File", "FileId")
