from functools import lru_cache

import enum
import inspect
import types
import typing
from functools import lru_cache

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.base import Node

    T = typing.TypeVar("T", bound=ABCRule)

Impl: typing.TypeAlias = type[classmethod]
FuncType: typing.TypeAlias = types.FunctionType | typing.Callable[..., typing.Any]

TRANSLATIONS_KEY: typing.Final[str] = "_translations"
IMPL_MARK: typing.Final[str] = "_is_impl"


def resolve_arg_names(func: FuncType, start_idx: int = 1) -> tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


@lru_cache(maxsize=65536)
def get_default_args(func: FuncType) -> dict[str, typing.Any]:
    fspec = inspect.getfullargspec(func)
    if not fspec.defaults:
        return {}
    return dict(zip(fspec.args[-len(fspec.defaults):], fspec.defaults))


def get_annotations(func: FuncType, *, return_type: bool = False) -> dict[str, typing.Any]:
    if not return_type and "return" in func.__annotations__:
        del func.__annotations__["return"]
    return func.__annotations__


def to_str(s: str | enum.Enum) -> str:
    if isinstance(s, enum.Enum):
        return str(s.value)
    return s


def magic_bundle(
    handler: FuncType,
    kw: dict[str | enum.Enum, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
) -> dict[str, typing.Any]:
    names = resolve_arg_names(handler, start_idx=start_idx)
    args = get_default_args(handler)
    args.update({to_str(k): v for k, v in kw.items() if to_str(k) in names})
    if "ctx" in names and bundle_ctx:
        args["ctx"] = kw
    return args


def get_cached_translation(rule: "T", locale: str) -> "T | None":
    return getattr(rule, TRANSLATIONS_KEY, {}).get(locale)


def cache_translation(base_rule: "T", locale: str, translated_rule: "T") -> None:
    translations = getattr(base_rule, TRANSLATIONS_KEY, {})
    translations[locale] = translated_rule
    setattr(base_rule, TRANSLATIONS_KEY, translations)


def get_impls(cls: type["Node"]) -> list[typing.Callable[..., typing.Any]]:
    return [
        func.__func__
        for func in vars(cls).values()
        if isinstance(func, classmethod) and getattr(func.__func__, IMPL_MARK, False)
    ]


@typing.cast(typing.Callable[..., Impl], lambda f: f)
def impl(method: typing.Callable[..., typing.Any]):
    bound_method = classmethod(method)
    setattr(method, IMPL_MARK, True)
    return bound_method


__all__ = (
    "TRANSLATIONS_KEY",
    "cache_translation",
    "get_annotations",
    "get_cached_translation",
    "get_default_args",
    "get_default_args",
    "impl",
    "magic_bundle",
    "resolve_arg_names",
    "to_str",
)
