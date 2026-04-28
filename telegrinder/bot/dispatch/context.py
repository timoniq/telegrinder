from __future__ import annotations

import typing
from reprlib import recursive_repr

from kungfu.library.monad.option import NOTHING, Option, Some
from nodnod.interface.node_from_function import Externals

if typing.TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem
    from nodnod.scope import Scope

    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.update import UpdateCute
    from telegrinder.bot.dispatch.router.base import Router
    from telegrinder.types.objects import Update

    type Key = str
    type Value = typing.Any

SELF_CONTEXT_KEYS: typing.Final = frozenset(("context", "ctx"))


class ContextKeyError(KeyError):
    def __str__(self) -> str:
        return BaseException.__str__(self)


class Context(Externals):
    """Low level per event mutable context storage."""

    if typing.TYPE_CHECKING:
        api: API
        update: Update
        raw_update: Update
        update_cute: UpdateCute
        per_event_scope: Scope
        exceptions_update: dict[Router, BaseException]
        exception_update: Option[BaseException]

        @typing.overload
        def __init__(self) -> None: ...

        @typing.overload
        def __init__(self, map: SupportsKeysAndGetItem[Key, Value], /) -> None: ...

        @typing.overload
        def __init__(self, **context: Value) -> None: ...

        def __init__(
            self,
            map: SupportsKeysAndGetItem[Key, Value] | None = None,
            **context: Value,
        ) -> None: ...

        def __setattr__(self, __key: Key, __value: Value) -> None: ...

        def __delattr__(self, __name: Key) -> None: ...

    else:
        __setattr__ = Externals.__setitem__
        __delattr__ = Externals.__delitem__

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(f"{k}={repr(v) if v is not self else '<self>'}" for k, v in self.items()),
        )

    def __getitem__(self, __key: Key) -> Value:
        if __key in SELF_CONTEXT_KEYS:
            return Externals.get(self, __key, self)

        try:
            return Externals.__getitem__(self, __key)
        except KeyError as error:
            raise ContextKeyError(f"`Context` does not have `{error.args[0]}` key.") from None

    __getattr__ = __getitem__

    def __contains__(self, __key: Key) -> bool:
        """Key in self."""
        return __key in SELF_CONTEXT_KEYS or Externals.__contains__(self, __key)

    def __or__(self, other: SupportsKeysAndGetItem[Key, Value], /) -> Context:
        Externals.update(new_context := self.copy(), other)
        return new_context

    def __ior__(self, other: SupportsKeysAndGetItem[Key, Value], /) -> typing.Self:
        Externals.update(self, other)
        return self

    def as_dict(self) -> dict[Key, Value]:
        """Return a context as a dict."""
        return dict(self)

    def add_roots(
        self,
        api: API,
        update: Update,
        per_event_scope: Scope,
        /,
    ) -> typing.Self:
        from telegrinder.bot.cute_types.update import UpdateCute

        self |= {
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
            "exception_update": NOTHING,
        }
        return self

    def add_exception_update(self, exception_update: BaseException, /) -> typing.Self:
        self.exception_update = Some(exception_update)
        return self

    def copy(self) -> Context:
        """Return a shallow copy of the Context."""
        return Context(self)

    set = Externals.__setitem__
    delete = Externals.__delitem__

    def get_or_set[Default](self, key: Key, default: Default, /) -> Default:
        """Return self[key] if exists, otherwise set self[key] to default and return it."""
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default


__all__ = ("Context",)
