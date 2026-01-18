import importlib.util as importlib_util
import os
import pathlib
import sys
import typing
from abc import ABC, abstractmethod

from telegrinder.api.api import API
from telegrinder.types.objects import Update


class PathExistsError(BaseException):
    pass


class ABCDispatch(ABC):
    @abstractmethod
    async def feed(self, api: API, update: Update) -> typing.Any:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass

    def load_many(self, *externals: typing.Self) -> None:
        for external in externals:
            self.load(external)

    def load_from_dir(
        self,
        directory: str | pathlib.Path,
        *,
        recursive: bool = False,
    ) -> bool:
        """Loads dispatchers from a directory containing Python modules where global variables
        are declared with instances of dispatch.
        Returns True if dispatchers were found, otherwise False.
        """

        directory = pathlib.Path(directory)

        if not directory.exists():
            raise PathExistsError(f"Path `{directory!s}` doesn't exists.")

        found = False
        files_iter = os.walk(directory) if recursive else [(directory, [], os.listdir(directory))]

        for root, _, files in files_iter:
            for f in files:
                if f.endswith(".py") and f != "__init__.py":
                    module_path = os.path.join(root, f)
                    relative_path = os.path.relpath(module_path, sys.path[0])
                    module_name = os.path.splitext(relative_path)[0].replace(os.sep, ".")

                    if module_name not in sys.modules:
                        spec = importlib_util.spec_from_file_location(module_name, module_path)
                        if spec is None or spec.loader is None:
                            continue

                        module = importlib_util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                    else:
                        module = sys.modules[module_name]

                    for obj in vars(module).values():
                        if isinstance(obj, type(self)):
                            found = True
                            self.load(obj)

        return found


__all__ = ("ABCDispatch",)
