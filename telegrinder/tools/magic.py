from __future__ import annotations

import enum
import inspect
import types
import typing
from functools import wraps

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.polymorphic import Polymorphic

type Impl = type[classmethod]
type FuncType = types.FunctionType | typing.Callable[..., typing.Any]

TRANSLATIONS_KEY: typing.Final[str] = "_translations"
IMPL_MARK: typing.Final[str] = "_is_impl"


def cache_magic_value(mark_key: str, /):
    def inner[Func: typing.Callable[..., typing.Any]](func: Func) -> Func:
        @wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            if mark_key not in args[0].__dict__:
                args[0].__dict__[mark_key] = func(*args, **kwargs)
            return args[0].__dict__[mark_key]

        return wrapper  # type: ignore

    return inner


def resolve_arg_names(func: FuncType, start_idx: int = 1) -> tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


@cache_magic_value("__default_args__")
def get_default_args(func: FuncType) -> dict[str, typing.Any]:
    kwdefaults = func.__kwdefaults__
    if kwdefaults:
        return kwdefaults

    defaults = func.__defaults__
    if not defaults:
        return {}

    return {k: defaults[i] for i, k in enumerate(resolve_arg_names(func, start_idx=0)[-len(defaults) :])}


@cache_magic_value("__func_parameters__")
def get_func_parameters(func: FuncType) -> FuncParams:
    func_params: FuncParams = {"args": [], "kwargs": []}

    for k, p in inspect.signature(func).parameters.items():
        if k in ("self", "cls"):
            continue

        match p.kind:
            case p.POSITIONAL_OR_KEYWORD | p.POSITIONAL_ONLY:
                func_params["args"].append((k, p.default))
            case p.KEYWORD_ONLY:
                func_params["kwargs"].append((k, p.default))
            case p.VAR_POSITIONAL:
                func_params["var_args"] = k
            case p.VAR_KEYWORD:
                func_params["var_kwargs"] = k

    return func_params


def get_annotations(func: FuncType, *, return_type: bool = False) -> dict[str, typing.Any]:
    annotations = func.__annotations__
    if not return_type:
        annotations.pop("return", None)
    return annotations


def to_str(s: str | enum.Enum) -> str:
    if isinstance(s, enum.Enum):
        return str(s.value)
    return s


@typing.overload
def magic_bundle(handler: FuncType, kw: dict[str, typing.Any]) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(handler: FuncType, kw: dict[enum.Enum, typing.Any]) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    handler: FuncType,
    kw: dict[str, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    handler: FuncType,
    kw: dict[enum.Enum, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    handler: FuncType,
    kw: dict[type[typing.Any], typing.Any],
    *,
    typebundle: typing.Literal[True] = True,
) -> dict[str, typing.Any]: ...


def magic_bundle(
    handler: FuncType,
    kw: dict[typing.Any, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
    typebundle: bool = False,
) -> dict[str, typing.Any]:
    if typebundle:
        return {name: kw[t] for name, t in get_annotations(handler, return_type=False).items() if t in kw}

    names = resolve_arg_names(handler, start_idx=start_idx)
    args = get_default_args(handler)
    args.update({to_str(k): v for k, v in kw.items() if to_str(k) in names})
    if "ctx" in names and bundle_ctx:
        args["ctx"] = kw
    return args


def get_cached_translation[Rule: ABCRule](rule: Rule, locale: str) -> Rule | None:
    return getattr(rule, TRANSLATIONS_KEY, {}).get(locale)


def cache_translation[Rule: ABCRule](
    base_rule: Rule,
    locale: str,
    translated_rule: Rule,
) -> None:
    translations = getattr(base_rule, TRANSLATIONS_KEY, {})
    translations[locale] = translated_rule
    setattr(base_rule, TRANSLATIONS_KEY, translations)


@typing.cast(typing.Callable[..., Impl], lambda f: f)
def impl(method: typing.Callable[..., typing.Any]):
    setattr(method, IMPL_MARK, True)
    return classmethod(method)


def get_impls(cls: type[Polymorphic]) -> list[typing.Callable[..., typing.Any]]:
    moprh_impls = getattr(cls, "__morph_impls__", None)
    if moprh_impls is not None:
        return moprh_impls
    impls = [
        func.__func__
        for func in vars(cls).values()
        if isinstance(func, classmethod) and getattr(func.__func__, IMPL_MARK, False)
    ]
    setattr(cls, "__morph_impls__", impls)
    return impls


class FuncParams(typing.TypedDict, total=True):
    args: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    kwargs: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    var_args: typing.NotRequired[str]
    var_kwargs: typing.NotRequired[str]


__all__ = (
    "TRANSLATIONS_KEY",
    "cache_magic_value",
    "cache_translation",
    "get_annotations",
    "get_cached_translation",
    "get_default_args",
    "get_default_args",
    "get_func_parameters",
    "get_impls",
    "impl",
    "magic_bundle",
    "resolve_arg_names",
    "to_str",
)
