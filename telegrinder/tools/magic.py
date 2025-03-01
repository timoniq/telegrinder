from __future__ import annotations

import asyncio
import dataclasses
import enum
import inspect
import typing
from collections import OrderedDict
from functools import wraps

from fntypes import Result

from telegrinder.model import get_params

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.polymorphic import Polymorphic

type Impl = type[classmethod]
type Function = typing.Callable[..., typing.Any]
type Executor[T] = typing.Callable[
    [T, str, dict[str, typing.Any]],
    typing.Awaitable[Result[typing.Any, typing.Any]],
]

TRANSLATIONS_KEY: typing.Final[str] = "_translations"
MORPH_IMPLEMENTATIONS_KEY = "__morph_implementations__"
IMPL_MARK: typing.Final[str] = "_is_impl"
CONTEXT_KEYS: typing.Final[tuple[str, ...]] = ("ctx", "context")


class FuncParams(typing.TypedDict, total=True):
    args: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    kwargs: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    var_args: typing.NotRequired[str]
    var_kwargs: typing.NotRequired[str]


@dataclasses.dataclass(slots=True, frozen=True)
class Shortcut[T]:
    method_name: str
    executor: Executor[T] | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set[str](), kw_only=True)


def cache_magic_value(mark_key: str, /):
    def inner[Func: typing.Callable[..., typing.Any]](func: Func) -> Func:
        @wraps(func)
        def wrapper(
            f: Function | None = None,
            /,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> typing.Any:
            if f is not None and mark_key not in f.__dict__:
                f.__dict__[mark_key] = func(f, *args, **kwargs)
            return f.__dict__[mark_key]

        return wrapper  # type: ignore

    return inner


def resolve_arg_names(func: Function, start_idx: int = 1) -> tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


@cache_magic_value("__default_arguments__")
def get_default_args(func: Function, /) -> dict[str, typing.Any]:
    defaults = func.__defaults__
    kwdefaults = {} if not func.__kwdefaults__ else func.__kwdefaults__.copy()
    if not defaults:
        return kwdefaults
    return {
        k: defaults[i] for i, k in enumerate(resolve_arg_names(func, start_idx=0)[-len(defaults) :])
    } | kwdefaults


@cache_magic_value("__function_parameters__")
def get_func_parameters(func: Function, /) -> FuncParams:
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


def get_annotations(func: Function, *, return_type: bool = False) -> dict[str, typing.Any]:
    annotations = func.__annotations__.copy()
    if not return_type:
        annotations.pop("return", None)
    return annotations


def to_str(s: str | enum.Enum) -> str:
    if isinstance(s, enum.Enum):
        return str(s.value)
    return s


@typing.overload
def magic_bundle(
    function: Function,
    kw: dict[str, typing.Any],
    *,
    start_idx: int = 1,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    function: Function,
    kw: dict[enum.Enum, typing.Any],
    *,
    start_idx: int = 1,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    function: Function,
    kw: dict[str, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    function: Function,
    kw: dict[enum.Enum, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]: ...


@typing.overload
def magic_bundle(
    function: Function,
    kw: dict[type[typing.Any], typing.Any],
    *,
    start_idx: int = 1,
    typebundle: typing.Literal[True] = True,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]: ...


def magic_bundle(
    function: Function,
    kw: dict[typing.Any, typing.Any],
    *,
    start_idx: int = 1,
    bundle_ctx: bool = True,
    typebundle: bool = False,
    omit_defaults: bool = False,
) -> dict[str, typing.Any]:
    # Bundle considering the function annotations
    if typebundle:
        return {name: kw[t] for name, t in get_annotations(function, return_type=False).items() if t in kw}

    names = resolve_arg_names(function, start_idx=start_idx)
    # Determine if the function is only have the **kwargs parameter, then bundle all kw
    if "var_kwargs" in get_func_parameters(function) and not names:
        return {to_str(k): v for k, v in kw.items()}

    # Bundle considering the function parameters and defaults (if do not omit defaults)
    defaults = {} if omit_defaults else get_default_args(function)
    args = defaults | {n: v for k, v in kw.items() if (n := to_str(k)) in names}

    # Bundle a context if context key specified in `names`
    if bundle_ctx:
        for key in CONTEXT_KEYS:
            if key in names:
                args[key] = kw
                break

    return args


def join_dicts[Key: typing.Hashable, Value](
    left_dict: dict[Key, typing.Any],
    right_dict: dict[typing.Any, Value],
) -> dict[Key, Value]:
    return {key: right_dict[type_key] for key, type_key in left_dict.items()}


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


def get_polymorphic_implemenations(cls: type[Polymorphic], /) -> list[typing.Callable[..., typing.Any]]:
    moprh_impls = getattr(cls, MORPH_IMPLEMENTATIONS_KEY, None)
    if moprh_impls is not None:
        return moprh_impls

    impls = []
    for cls_ in cls.mro():
        impls += [
            obj.__func__
            for obj in vars(cls_).values()
            if isinstance(obj, classmethod) and getattr(obj.__func__, IMPL_MARK, False)
        ]

    setattr(cls, MORPH_IMPLEMENTATIONS_KEY, impls)
    return impls


def shortcut[T](
    method_name: str,
    *,
    executor: Executor[T] | None = None,
    custom_params: set[str] | None = None,
):
    """Decorate a cute method as a shortcut."""

    def wrapper[F: typing.Callable[..., typing.Any]](func: F) -> F:
        @wraps(func)
        async def inner(
            self: T,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> typing.Any:
            if executor is None:
                return await func(self, *args, **kwargs)

            params: dict[str, typing.Any] = OrderedDict()
            func_params = get_func_parameters(func)

            for index, (arg, default) in enumerate(func_params["args"]):
                if len(args) > index:
                    params[arg] = args[index]
                elif default is not inspect.Parameter.empty:
                    params[arg] = default

            if var_args := func_params.get("var_args"):
                params[var_args] = args[len(func_params["args"]) :]

            for kwarg, default in func_params["kwargs"]:
                params[kwarg] = (
                    kwargs.pop(kwarg, default) if default is not inspect.Parameter.empty else kwargs.pop(kwarg)
                )

            if var_kwargs := func_params.get("var_kwargs"):
                params[var_kwargs] = kwargs.copy()

            return await executor(self, method_name, get_params(params))

        inner.__shortcut__ = Shortcut(  # type: ignore
            method_name=method_name,
            executor=executor,
            custom_params=custom_params or set(),
        )
        return inner  # type: ignore

    return wrapper


# Source code: https://github.com/facebookincubator/later/blob/main/later/task.py#L75
async def cancel_future(fut: asyncio.Future[typing.Any], /) -> None:
    if fut.done():
        return

    fut.cancel()
    exc: asyncio.CancelledError | None = None

    while not fut.done():
        shielded = asyncio.shield(fut)
        try:
            await asyncio.wait([shielded])
        except asyncio.CancelledError as ex:
            exc = ex
        finally:
            # Insure we handle the exception/value that may exist on the shielded task
            # This will prevent errors logged to the asyncio logger
            if shielded.done() and not shielded.cancelled() and not shielded.exception():
                shielded.result()

    if fut.cancelled():
        if exc is None:
            return
        raise exc from None

    ex = fut.exception()
    if ex is not None:
        raise ex from None

    raise asyncio.InvalidStateError(
        f"Task did not raise CancelledError on cancel: {fut!r} had result {fut.result()!r}",
    )


__all__ = (
    "Shortcut",
    "TRANSLATIONS_KEY",
    "cache_magic_value",
    "cache_translation",
    "cancel_future",
    "get_annotations",
    "get_cached_translation",
    "get_default_args",
    "get_default_args",
    "get_func_parameters",
    "get_polymorphic_implemenations",
    "impl",
    "join_dicts",
    "magic_bundle",
    "resolve_arg_names",
    "shortcut",
    "to_str",
)
