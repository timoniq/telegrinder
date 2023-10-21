import enum
import inspect
import types
import typing

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

    T = typing.TypeVar("T", bound=ABCRule)

FuncType = types.FunctionType | typing.Callable
TRANSLATIONS_KEY = "_translations"


def resolve_arg_names(func: FuncType) -> tuple[str, ...]:
    return func.__code__.co_varnames[1 : func.__code__.co_argcount]


def get_default_args(func: FuncType) -> dict[str, typing.Any]:
    fspec = inspect.getfullargspec(func)
    return dict(zip(fspec.args[::-1], (fspec.defaults or ())[::-1]))


def to_str(s: str | enum.Enum) -> str:
    if isinstance(s, enum.Enum):
        return s.value
    return s


def magic_bundle(
    handler: FuncType, kw: dict[str | enum.Enum, typing.Any]
) -> dict[str, typing.Any]:
    names = resolve_arg_names(handler)
    args = get_default_args(handler)
    args.update({to_str(k): v for k, v in kw.items() if to_str(k) in names})
    if "ctx" in names:
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
