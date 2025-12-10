from __future__ import annotations

import enum
import types
import typing
from reprlib import recursive_repr

from kungfu.library.monad.option import Nothing, Option, Some

if typing.TYPE_CHECKING:
    from _collections_abc import dict_keys

    from nodnod.scope import Scope

    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.update import UpdateCute
    from telegrinder.bot.dispatch.router.base import Router
    from telegrinder.types.objects import Update

type Key = str | enum.Enum
type AnyValue = typing.Any

Opt = Some | Nothing
ContextDict = dict[str, AnyValue]

NOTHING: typing.Final = Nothing()


class RootKey(str):
    pass


class AliasKey(str):
    key: str

    def __new__(cls, alias: str, key: str, /) -> typing.Self:
        instance = super().__new__(cls, alias)
        instance.key = key
        return instance


class ContextKeyError(KeyError):
    def __str__(self) -> str:
        return str(self.args[0] if len(self.args) == 1 else (self.args or ""))


class Context(ContextDict):
    """Low level per event context storage."""

    __roots__: typing.ClassVar = (
        RootKey("api"),
        RootKey("raw_update"),
        RootKey("update_cute"),
        RootKey("per_event_scope"),
    )
    __unpack_aliases__: typing.ClassVar = types.MappingProxyType(  # Aliases for unpacking context via **
        mapping=dict(
            raw_update="update",
            context="ctx",
        ),
    )

    exceptions_update: dict[Router, Exception]
    api: Option[API] = NOTHING
    raw_update: Option[Update] = NOTHING
    update_cute: Option[UpdateCute] = NOTHING
    per_event_scope: Option[Scope] = NOTHING
    exception_update: Option[Exception] = NOTHING

    def __init__(self, **kwargs: AnyValue) -> None:
        kwargs.setdefault("exceptions_update", dict())
        self.set_roots(kwargs)
        dict.__init__(self, **kwargs)
        self.context = self

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__, ", ".join(f"{k}={repr(v) if v is not self else '<self>'}" for k, v in self.items())
        )

    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        dict.__setitem__(self, self.key_to_str(__key), __value)

    def __getitem__(self, __key: Key) -> AnyValue:
        if isinstance(__key, AliasKey):
            __key = __key.key

        value = dict.__getitem__(self, self.key_to_str(__key))

        if isinstance(__key, RootKey) and isinstance(value, Opt):
            value = value.expect(ContextKeyError(f"Root value for key `{__key}` is none."))

        return value

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

    def __or__(self, other: object, /) -> typing.Self:
        if not isinstance(other, Context):
            return NotImplemented

        roots: dict[str, AnyValue] = {}

        for key, val in self.items():
            if key in self.__roots__ and not isinstance(val, Nothing | types.NoneType):
                roots[key] = val

        return type(self)(**{**roots, **self.as_dict(), **other.as_dict()})

    def __ior__(self, other: object, /) -> typing.Self:
        return self.__or__(other)

    def keys(self) -> dict_keys[str, AnyValue]:
        context_cls = type(self)
        keys: list[str] = []

        for key in ContextDict.keys(self):
            if key in context_cls.__roots__:
                key = context_cls.__roots__[context_cls.__roots__.index(key)]

            keys.append(key)

            if (alias_key := context_cls.__unpack_aliases__.get(key)) is not None:
                keys.append(AliasKey(alias_key, key))

        return dict.fromkeys(keys).keys()

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.keys())

    def as_dict(self) -> dict[str, AnyValue]:
        return {key: value for key, value in ContextDict.items(self) if key not in self.__roots__}

    def add_roots(
        self,
        api: API,
        update: Update,
        per_event_scope: Scope,
        /,
    ) -> typing.Self:
        from telegrinder.bot.cute_types.update import UpdateCute

        context_cls = type(self)

        if context_cls not in per_event_scope:
            per_event_scope.inject(context_cls, self)

        self.set_roots(
            roots={
                "api": api,
                "raw_update": update,
                "update_cute": UpdateCute.from_update(update, bound_api=api),
                "per_event_scope": per_event_scope,
            },
        )
        return self

    def add_exception_update(self, exception_update: Exception, /) -> typing.Self:
        self.exception_update = Some(exception_update)
        return self

    @staticmethod
    def key_to_str(key: Key) -> str:
        return key if isinstance(key, str) else str(key.value)

    def copy(self) -> typing.Self:
        return type(self)(**ContextDict.copy(self.as_dict()))

    def update(self, other: Context, /) -> None:
        if not isinstance(other, Context):
            raise TypeError(f"Cannot update Context with {type(other).__name__}")

        self |= other

    def set(self, key: Key, value: AnyValue) -> None:
        self[key] = value

    def set_roots(self, roots: dict[str, AnyValue]) -> None:
        for root in self.__roots__:
            if root in roots:
                root_value = roots.pop(root)
                self[root] = Some(root_value) if not isinstance(root_value, Opt) else root_value
            else:
                self[root] = NOTHING

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
