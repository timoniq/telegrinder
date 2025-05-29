from __future__ import annotations

import enum
import typing
from reprlib import recursive_repr

from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.node.composer import NodeCollection

type Key = str | enum.Enum
type AnyValue = typing.Any


class Context(dict[str, AnyValue]):
    """Per-event the context storage."""

    raw_update: Update
    exception_update: BaseException | None = None
    node_col: NodeCollection | None = None

    def __init__(self, **kwargs: AnyValue) -> None:
        cls_vars = vars(self.__class__)
        defaults = {}

        for k in self.__class__.__annotations__:
            if k in cls_vars:
                defaults[k] = cls_vars[k]
                delattr(self.__class__, k)

        dict.__init__(self, **defaults | kwargs)

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, ", ".join(f"{k}={v!r}" for k, v in self.items()))

    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        dict.__setitem__(self, self.key_to_str(__key), __value)

    def __getitem__(self, __key: Key) -> AnyValue:
        return dict.__getitem__(self, self.key_to_str(__key))

    def __delitem__(self, __key: Key) -> None:
        dict.__delitem__(self, self.key_to_str(__key))

    def __setattr__(self, __name: str, __value: AnyValue) -> None:
        self.__setitem__(__name, __value)

    def __getattr__(self, __name: str) -> AnyValue:
        return self.__getitem__(__name)

    def __delattr__(self, __name: str) -> None:
        self.__delitem__(__name)

    @staticmethod
    def key_to_str(key: Key) -> str:
        return key if isinstance(key, str) else str(key.value)

    def copy(self) -> typing.Self:
        return self.__class__(**dict.copy(self))

    def set(self, key: Key, value: AnyValue) -> None:
        self[key] = value

    @typing.overload
    def get(self, key: Key) -> AnyValue | None: ...

    @typing.overload
    def get[T](self, key: Key, default: T) -> T | AnyValue: ...

    @typing.overload
    def get(self, key: Key, default: None = None) -> AnyValue | None: ...

    def get[T](self, key: Key, default: T | None = None) -> T | AnyValue | None:
        return dict.get(self, key, default)

    def get_or_set[T](self, key: Key, default: T) -> T:
        if key not in self:
            self.set(key, default)
        return self.get(key, default)

    def delete(self, key: Key) -> None:
        del self[key]


__all__ = ("Context",)
