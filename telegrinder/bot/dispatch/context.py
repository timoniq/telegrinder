from __future__ import annotations

import typing
from reprlib import recursive_repr

from kungfu.library.monad.option import NOTHING, Option, Some
from nodnod.interface.node_from_function import Externals

if typing.TYPE_CHECKING:
    from nodnod.scope import Scope

    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.update import UpdateCute
    from telegrinder.bot.dispatch.router.base import Router
    from telegrinder.types.objects import Update

type Key = str
type AnyValue = typing.Any

SELF_CONTEXT_KEYS: typing.Final = frozenset(("context", "ctx"))


class Context(Externals):
    """Low level per event context storage."""

    api: API
    update: Update
    raw_update: Update
    update_cute: UpdateCute
    per_event_scope: Scope
    exceptions_update: dict[Router, Exception]
    exception_update: Option[Exception] = NOTHING

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, map: typing.Mapping[Key, AnyValue], /) -> None: ...

    @typing.overload
    def __init__(self, **kwargs: AnyValue) -> None: ...

    def __init__(
        self,
        map: typing.Mapping[Key, AnyValue] | None = None,
        **kwargs: AnyValue,
    ) -> None:
        Externals.__init__(self, map or kwargs)

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(f"{k}={repr(v) if v is not self else '<self>'}" for k, v in self.items()),
        )

    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        Externals.__setitem__(self, __key, __value)

    def __getitem__(self, __key: Key) -> AnyValue:
        if __key in SELF_CONTEXT_KEYS:
            return self
        return Externals.__getitem__(self, __key)

    def __delitem__(self, __key: Key) -> None:
        Externals.__delitem__(self, __key)

    def __setattr__(self, __name: str, __value: AnyValue) -> None:
        self.__setitem__(__name, __value)

    def __getattribute__(self, __name: str) -> AnyValue:
        if __name in SELF_CONTEXT_KEYS:
            return self

        if __name in _CONTEXT_CLASS_ATTRS and not Externals.__contains__(self, __name):
            return super().__getattribute__(__name)

        return self[__name]

    def __delattr__(self, __name: str) -> None:
        self.__delitem__(__name)

    def __contains__(self, __key: object) -> bool:
        if __key in SELF_CONTEXT_KEYS:
            return True
        return Externals.__contains__(self, __key)

    def __or__(self, other: object, /) -> typing.Self:
        if type(other) is not Context and not isinstance(other, dict):
            return NotImplemented

        new_context = type(self)(self)
        new_context |= other
        return new_context

    def __ior__(self, other: object, /) -> typing.Self:
        if type(other) is not Context and not isinstance(other, dict):
            raise TypeError(f"Cannot update `Context` with `{type(other).__name__}`.")

        for key, value in other.items():
            self[key] = value

        return self

    def as_dict(self) -> dict[Key, AnyValue]:
        return {key: value for key, value in Externals.items(self)}

    def add_roots(
        self,
        api: API,
        update: Update,
        per_event_scope: Scope,
        /,
    ) -> typing.Self:
        from telegrinder.bot.cute_types.update import UpdateCute

        for key, value in {
            "api": api,
            "raw_update": update,
            "update": update,
            "update_cute": (
                update.bind(update, api)
                if isinstance(update, UpdateCute)
                else UpdateCute.from_update(update, bound_api=api)
            ),
            "per_event_scope": per_event_scope,
            "exceptions_update": {},
        }.items():
            self[key] = value

        return self

    def add_exception_update(self, exception_update: Exception, /) -> typing.Self:
        self.exception_update = Some(exception_update)
        return self

    def copy(self) -> typing.Self:
        return type(self)(self)

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


_CONTEXT_CLASS_ATTRS: typing.Final = frozenset(Context.__dict__ | Externals.__dict__ | dict.__dict__ | object.__dict__)


__all__ = ("Context",)
