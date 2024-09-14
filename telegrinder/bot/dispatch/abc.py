import importlib.util as importlib_util
import os
import pathlib
import sys
import typing
from abc import ABC, abstractmethod

from fntypes.option import Option

from telegrinder.api.api import API
from telegrinder.tools.global_context.abc import ABCGlobalContext
from telegrinder.types.objects import Update

T = typing.TypeVar("T")


class PathExistsError(BaseException):
    pass


class ABCDispatch(ABC):
    @property
    @abstractmethod
    def global_context(self) -> ABCGlobalContext:
        pass

    @abstractmethod
    async def feed(self, event: Update, api: API) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass

    @abstractmethod
    def get_view(self, of_type: type[T]) -> Option[T]:
        pass

    def load_many(self, *externals: typing.Self) -> None:
        for external in externals:
            self.load(external)

    def load_from_dir(self, directory: str | pathlib.Path) -> bool:
        """Loads dispatchers from a directory containing Python modules where global variables
        are declared with instances of dispatch.
        Returns True if dispatchers were found, otherwise False."""

        directory = pathlib.Path(directory)

        if not directory.exists():
            raise PathExistsError(f"Path {str(directory)!r} does not exists.")

        dps: list[typing.Self] = []
        for root, _, files in os.walk(directory):
            for f in files:
                if f.endswith(".py") and f != "__init__.py":
                    module_path = os.path.join(root, f)
                    module_name = os.path.splitext(os.path.relpath(module_path, directory))[0]
                    module_name = module_name.replace(os.sep, ".")

                    spec = importlib_util.spec_from_file_location(module_name, module_path)
                    if spec is None or spec.loader is None:
                        continue

                    module = importlib_util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    for obj in module.__dict__.values():
                        if isinstance(obj, self.__class__):
                            dps.append(obj)

        self.load_many(*dps)
        return bool(dps)


__all__ = ("ABCDispatch",)
