import dataclasses
import pathlib

from telegrinder.types.objects import InputFile


@dataclasses.dataclass
class InputFileManager:
    directory: pathlib.Path
    storage: dict[str, InputFile] = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.storage = self._load_files()

    def _load_files(self) -> dict[str, InputFile]:
        files = {}

        for path in self.directory.rglob("*"):
            if path.is_file():
                relative_path = path.relative_to(self.directory)
                files[str(relative_path)] = InputFile(path.name, path.read_bytes())

        return files

    def get(self, filename: str, /) -> InputFile:
        assert filename in self.storage, f"File {filename!r} not found."
        return self.storage[filename]


__all__ = ("InputFileManager",)
