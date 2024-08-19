import enum
import inspect
import types
import typing
from functools import wraps

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.base import Node

    T = typing.TypeVar("T", bound=ABCRule)
    F = typing.TypeVar(
        "F",
        bound=typing.Callable[typing.Concatenate[typing.Callable[..., typing.Any], ...], typing.Any],
    )

Impl: typing.TypeAlias = type[classmethod]
NodeImpl: typing.TypeAlias = Impl
FuncType: typing.TypeAlias = types.FunctionType | typing.Callable[..., typing.Any]

TRANSLATIONS_KEY: typing.Final[str] = "_translations"
IMPL_MARK: typing.Final[str] = "_is_impl"
NODE_IMPL_MARK: typing.Final[str] = "_is_node_impl"


def cache_magic_value(mark_key: str, /):
    def inner(func: "F") -> "F":
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


@typing.overload
def magic_bundle(handler: FuncType, kw: dict[str, typing.Any]) -> dict[str, typing.Any]:
    ...


@typing.overload
def magic_bundle(handler: FuncType, kw: dict[enum.Enum, typing.Any]) -> dict[str, typing.Any]:
    ...


@typing.overload
def magic_bundle(
    handler: FuncType,
    kw: dict[str, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
) -> dict[str, typing.Any]:
    ...


@typing.overload
def magic_bundle(
    handler: FuncType,
    kw: dict[enum.Enum, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
) -> dict[str, typing.Any]:
    ...


def magic_bundle(
    handler: FuncType,
    kw: dict[typing.Any, typing.Any],
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


def get_impls_by_key(cls: type["Node"], mark_key: str) -> dict[str, typing.Callable[..., typing.Any]]:
    return {
        name: func.__func__
        for name, func in vars(cls).items()
        if isinstance(func, classmethod) and getattr(func.__func__, mark_key, False)
    }


@typing.cast(typing.Callable[..., Impl], lambda f: f)
def impl(method: typing.Callable[..., typing.Any]):
    setattr(method, IMPL_MARK, True)
    return classmethod(method)


@typing.cast(typing.Callable[..., NodeImpl], lambda f: f)
def node_impl(method: typing.Callable[..., typing.Any]):
    setattr(method, NODE_IMPL_MARK, True)
    return classmethod(method)


__all__ = (
    "TRANSLATIONS_KEY",
    "cache_magic_value",
    "cache_translation",
    "get_annotations",
    "get_cached_translation",
    "get_default_args",
    "get_default_args",
    "impl",
    "magic_bundle",
    "node_impl",
    "resolve_arg_names",
    "to_str",
)
