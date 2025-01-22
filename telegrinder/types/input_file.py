import pathlib
import secrets
import typing

from telegrinder.msgspec_utils import encoder

type Files = dict[str, tuple[str, bytes]]


class InputFile:
    """Object `InputFile`, see the [documentation](https://core.telegram.org/bots/api#inputfile).

    This object represents the contents of a file to be uploaded. Must be posted using `multipart/form-data` in the usual way that files are uploaded via the browser.
    """

    __slots__ = ("filename", "data")

    filename: str
    """File name."""

    data: bytes
    """Bytes of file."""

    def __init__(self, filename: str, data: bytes, /) -> None:
        self.filename = filename
        self.data = data

    def __repr__(self) -> str:
        return "{}(filename={!r}, data={!r})".format(
            self.__class__.__name__,
            self.filename,
            (self.data[:30] + b"...") if len(self.data) > 30 else self.data,
        )

    @classmethod
    def from_path(cls, path: str | pathlib.Path, /) -> typing.Self:
        path = pathlib.Path(path)
        return cls(path.name, path.read_bytes())

    def _to_multipart(self, files: Files, /) -> str:
        attach_name = secrets.token_urlsafe(16)
        files[attach_name] = (self.filename, self.data)
        return f"attach://{attach_name}"


@encoder.add_enc_hook(InputFile)
def encode_inputfile(inputfile: InputFile, files: Files) -> str:
    return inputfile._to_multipart(files)


__all__ = ("InputFile",)
