import dataclasses
import pathlib
import typing
from functools import cached_property

import msgspec
from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile

type Path = str | pathlib.Path


@dataclasses.dataclass
class ConfigTOML:
    file: TOMLFile

    @cached_property
    def document(self) -> TOMLDocument:
        return self.file.read()

    def save(self) -> None:
        self.file.write(data=self.document)

    def as_model[T: msgspec.Struct](
        self,
        model_type: type[T],
        /,
        *,
        dec_hook: typing.Callable[[type[typing.Any], typing.Any], typing.Any] | None = None,
    ) -> T:
        return msgspec.convert(self.document.unwrap(), type=model_type, dec_hook=dec_hook)


def read_config(path: Path, /) -> ConfigTOML:
    return ConfigTOML(file=TOMLFile(path))


__all__ = ("ConfigTOML", "read_config")
