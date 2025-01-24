from telegrinder.api.api import API
from telegrinder.types.objects import File as FileObject

from telegrinder.node.base import ComposeError, Node
from telegrinder.node.polymorphic import Polymorphic, impl
from telegrinder.node.attachment import Document, Video, Audio, Photo

class FileId(Polymorphic, str):
    @impl
    def compose_document(cls, document: Document) -> str:
        return document.file_id

    @impl
    def compose_video(cls, video: Video) -> str:
        return video.file_id

    @impl
    def compose_audio(cls, audio: Audio) -> str:
        return audio.file_id

    @impl
    def compose_photo(cls, photo: Photo) -> str:
        # last size is the best resolution
        return photo.sizes[-1].file_id

class File(Node, FileObject):
    @classmethod
    async def compose(cls, file_id: FileId, api: API) -> FileObject:
        file = await api.get_file(file_id=file_id)
        return file.expect(ComposeError("File can't be downloaded"))
