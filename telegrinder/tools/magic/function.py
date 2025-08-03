from __future__ import annotations

import dataclasses
import enum
import inspect
import types
import typing
from functools import cache, cached_property, wraps

from telegrinder.tools.magic.annotations import Annotations, MappingAnnotations

type Function[**P, R] = typing.Callable[P, R]
type AnyFunction = Function[..., typing.Any]


def _to_str(obj: typing.Any, /) -> str:
    if isinstance(obj, enum.Enum):
        return str(obj.value)
    return str(obj) if not isinstance(obj, str) else obj


def _resolve_arg_names(
    func: AnyFunction,
    /,
    *,
    start_idx: int,
    stop_idx: int,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    exclude = exclude or set()
    varnames = func.__code__.co_varnames[start_idx:stop_idx]
    return tuple(name for name in varnames if name not in exclude)


class FunctionParameters(typing.TypedDict):
    args: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    kwargs: list[tuple[str, typing.Any | inspect.Parameter.empty]]
    var_star_args: typing.NotRequired[str]
    var_star_kwargs: typing.NotRequired[str]


@dataclasses.dataclass(frozen=True, repr=False)
class Bundle[R]:
    function: Function[..., R]
    start_idx: int
    context: types.MappingProxyType[str, typing.Any]

    @cached_property
    def args(self) -> tuple[typing.Any, ...]:
        return tuple(
            self.context[name]
            for name in resolve_posonly_arg_names(self.function, start_idx=self.start_idx)
            if name in self.context
        )

    @cached_property
    def kwargs(self) -> dict[str, typing.Any]:
        posonly_arg_names = resolve_posonly_arg_names(self.function, start_idx=self.start_idx)
        return {name: value for name, value in self.context.items() if name not in posonly_arg_names}

    @classmethod
    def from_context(
        cls,
        function: Function[..., R],
        context: typing.Mapping[str, typing.Any],
        /,
        *,
        start_idx: int = 1,
    ) -> typing.Self:
        return cls(function, start_idx, types.MappingProxyType(context))

    def __repr__(self) -> str:
        return "<{}: function={!r} bundle args={!r} kwargs={!r}>".format(
            type(self).__name__,
            self.function,
            self.args,
            self.kwargs,
        )

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> R:
        return self.function(*args, *self.args, **kwargs, **self.kwargs)

    def __and__(self, other: object, /) -> typing.Self:
        if not isinstance(other, Bundle):
            return NotImplemented

        if self.function != other.function:
            raise ValueError(
                f"Cannot merge contexts because bundle {other!r} is intended for a different function.",
            )

        return dataclasses.replace(
            self,
            context=types.MappingProxyType(mapping=self.context | other.context),
        )

    def __iand__(self, other: object, /) -> typing.Self:
        return self.__and__(other)


def function_context[**P, R](key: str, /) -> Function[[Function[P, R]], Function[P, R]]:
    @lambda wrapper: typing.cast("Function[[Function[P, R]], Function[P, R]]", wrapper)
    def wrapper(func: Function[typing.Concatenate[AnyFunction, P], R], /) -> AnyFunction:
        @wraps(func)
        def inner(passed_function: AnyFunction, /, *args: P.args, **kwargs: P.kwargs) -> R:
            sentinel = object()
            context: dict[str, typing.Any] = passed_function.__dict__.setdefault("__function_context__", {})

            if (value := context.get(key, sentinel)) is not sentinel:
                return value

            context[key] = result = func(passed_function, *args, **kwargs)
            return result

        return inner

    return wrapper


def resolve_arg_names(
    func: AnyFunction,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=start_idx,
        stop_idx=func.__code__.co_argcount + func.__code__.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_kwonly_arg_names(
    func: AnyFunction,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=func.__code__.co_argcount + start_idx,
        stop_idx=func.__code__.co_argcount + func.__code__.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_posonly_arg_names(
    func: AnyFunction,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=start_idx,
        stop_idx=func.__code__.co_posonlyargcount,
        exclude=exclude,
    )


@cache
def get_default_args(func: AnyFunction, /) -> dict[str, typing.Any]:
    parameters = get_func_parameters(func)
    return {
        key: value
        for sublist in (parameters["args"], parameters["kwargs"])
        for key, value in sublist
        if value is not inspect.Parameter.empty
    }


@cache
def get_func_parameters(func: AnyFunction, /) -> FunctionParameters:
    func_params = FunctionParameters(args=[], kwargs=[])

    for k, p in inspect.signature(func).parameters.items():
        if k in ("self", "cls"):
            continue

        match p.kind:
            case p.POSITIONAL_OR_KEYWORD | p.POSITIONAL_ONLY:
                func_params["args"].append((k, p.default))
            case p.KEYWORD_ONLY:
                func_params["kwargs"].append((k, p.default))
            case p.VAR_POSITIONAL:
                func_params["var_star_args"] = k
            case p.VAR_KEYWORD:
                func_params["var_star_kwargs"] = k

    return func_params


@cache
def get_func_annotations(func: AnyFunction, /) -> MappingAnnotations:
    return Annotations(obj=func).get(
        ignore_failed_evals=True,
        exclude_forward_refs=True,
        cache=False,
    )


def bundle[R](
    function: Function[..., R],
    context: dict[typing.Any, typing.Any],
    /,
    *,
    start_idx: int = 1,
    bundle_kwargs: bool = False,
    typebundle: bool = False,
    omit_defaults: bool = False,
) -> Bundle[R]:
    if typebundle:
        return Bundle.from_context(
            function,
            {name: context[ann] for name, ann in get_func_annotations(function).items() if ann in context},
            start_idx=start_idx,
        )

    kwargs = {_to_str(k): v for k, v in context.items()}
    if not bundle_kwargs or "var_star_kwargs" not in get_func_parameters(function):
        names = resolve_arg_names(function, start_idx=start_idx, exclude={"cls", "self"})
        kwargs = {k: v for k, v in kwargs.items() if k in names}

    return Bundle.from_context(
        function,
        kwargs if omit_defaults else get_default_args(function) | kwargs,
        start_idx=start_idx,
    )


__all__ = (
    "Bundle",
    "bundle",
    "function_context",
    "get_default_args",
    "get_func_annotations",
    "get_func_parameters",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
)
