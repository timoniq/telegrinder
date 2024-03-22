import enum
import inspect
import types
import typing

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

    T = typing.TypeVar("T", bound=ABCRule)

FuncType: typing.TypeAlias = types.FunctionType | typing.Callable[..., typing.Any]
TRANSLATIONS_KEY = "_translations"


def resolve_arg_names(func: FuncType, start_idx: int = 1) -> tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


def get_default_args(func: FuncType) -> dict[str, typing.Any]:
    fspec = inspect.getfullargspec(func)
    return dict(zip(fspec.args[::-1], (fspec.defaults or ())[::-1]))


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


def get_cached_translation(rule: "T", locale: str) -> typing.Optional["T"]:
    translations = getattr(rule, TRANSLATIONS_KEY, {})
    if not translations or locale not in translations:
        return None
    return translations[locale]


def cache_translation(base_rule: "T", locale: str, translated_rule: "T") -> None:
    translations = getattr(base_rule, TRANSLATIONS_KEY, {})
    setattr(base_rule, TRANSLATIONS_KEY, {locale: translated_rule, **translations})


__all__ = (
    "TRANSLATIONS_KEY",
    "cache_translation",
    "get_cached_translation",
    "get_default_args",
    "get_default_args",
    "magic_bundle",
    "resolve_arg_names",
    "to_str",
)
