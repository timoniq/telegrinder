from __future__ import annotations

import enum
import typing
from reprlib import recursive_repr

from fntypes.option import Nothing, Option, Some

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.update import UpdateCute
    from telegrinder.types.objects import Update

type Key = str | enum.Enum
type AnyValue = typing.Any


class Context(dict[str, AnyValue]):
    """Low level per event context storage."""

    update_cute: Option[UpdateCute] = Nothing()
    exception_update: Option[BaseException] = Nothing()

    def __init__(self, **kwargs: AnyValue) -> None:
        dict.__init__(self, **kwargs)

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join(f"{k}={v!r}" for k, v in self.items()))

    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        dict.__setitem__(self, self.key_to_str(__key), __value)

    def __getitem__(self, __key: Key) -> AnyValue:
        return dict.__getitem__(self, self.key_to_str(__key))

    def __delitem__(self, __key: Key) -> None:
        dict.__delitem__(self, self.key_to_str(__key))

    def __setattr__(self, __name: str, __value: AnyValue) -> None:
        self.__setitem__(__name, __value)

    def __getattribute__(self, __name: str) -> AnyValue:
        cls = type(self)

        if __name in cls.__annotations__:
            return self[__name] if __name in self else super().__getattribute__(__name)

        if __name in _CONTEXT_CLASS_ATTRS:
            return super().__getattribute__(__name)

        return self.__getitem__(__name)

    def __delattr__(self, __name: str) -> None:
        self.__delitem__(__name)

    def add_update_cute(self, update: Update, bound_api: API, /) -> typing.Self:
        from telegrinder.bot.cute_types.update import UpdateCute

        self.update_cute = Some(UpdateCute.from_update(update, bound_api))
        return self

    def add_exception_update(self, exception_update: BaseException, /) -> typing.Self:
        self.exception_update = Some(exception_update)
        return self

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


_CONTEXT_CLASS_ATTRS = frozenset(Context.__dict__ | dict.__dict__ | object.__dict__)


__all__ = ("Context",)
