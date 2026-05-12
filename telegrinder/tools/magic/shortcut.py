import dataclasses
import inspect
import typing
from collections import OrderedDict
from functools import cache, wraps

from kungfu.library.monad.result import Result

from telegrinder.tools.magic.function import get_func_parameters

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError
    from telegrinder.bot.cute_types.base import BaseCute, BaseShortcuts

type Executor[T] = typing.Callable[
    [T, str, dict[str, typing.Any], typing.Any],
    typing.Awaitable[Result[typing.Any, APIError]],
]
type CuteMethod[T, **P, R] = typing.Callable[
    typing.Concatenate[T, P],
    typing.Awaitable[Result[R, APIError]],
]
type ShortcutMethod[**P, R] = typing.Callable[
    typing.Concatenate[typing.Any, P],
    typing.Coroutine[typing.Any, typing.Any, Result[R, APIError]],
]


@dataclasses.dataclass(slots=True, frozen=True)
class Shortcut[T]:
    method_name: str
    executor: Executor[T] | None = dataclasses.field(default=None, kw_only=True)
    return_type: typing.Any | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set[str](), kw_only=True)


@cache
def resolve_shortcut_result_type(result_type: typing.Any, /) -> typing.Any:
    if result_type is None:
        return typing.Any

    return typing.get_args(result_type)[0] if typing.get_origin(result_type) is Result else result_type


def get_shortcut_result_type(func: typing.Callable[..., typing.Any], /) -> typing.Any:
    return resolve_shortcut_result_type(func.__annotations__.get("return"))


@typing.overload
def shortcut[T: BaseCute, S: BaseShortcuts, **P, R](
    method_name: str,
    /,
    *,
    custom_params: set[str] = ...,
) -> typing.Callable[[CuteMethod[T, P, R] | CuteMethod[S, P, R]], ShortcutMethod[P, R]]: ...


@typing.overload
def shortcut[T: BaseCute, S: BaseShortcuts, **P, R](
    method_name: str,
    /,
    *,
    executor: Executor[T],
    return_type: typing.Any = ...,
    custom_params: set[str] = ...,
) -> typing.Callable[[CuteMethod[T, P, R] | CuteMethod[S, P, R]], ShortcutMethod[P, R]]: ...


def shortcut[**P, R](
    method_name: str,
    /,
    *,
    executor: Executor[typing.Any] | None = None,
    return_type: typing.Any | None = None,
    custom_params: set[str] | None = None,
) -> typing.Callable[[CuteMethod[typing.Any, P, R]], ShortcutMethod[P, R]]:
    """Decorate a cute method as a shortcut."""

    def wrapper(func: CuteMethod[typing.Any, P, R]) -> ShortcutMethod[P, R]:
        result_type: typing.Any | None = return_type

        @wraps(func)
        async def inner(
            self: typing.Any,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Result[R, typing.Any]:
            if executor is None:
                return await func(self, *args, **kwargs)

            params: dict[str, typing.Any] = OrderedDict()
            func_params = get_func_parameters(func)

            for index, (arg, default) in enumerate(func_params["args"]):
                if len(args) > index:
                    params[arg] = args[index]
                elif default is not inspect.Parameter.empty:
                    params[arg] = default

            if var_args := func_params.get("var_star_args"):
                params[var_args] = args[len(func_params["args"]) :]

            for kwarg, default in func_params["kwargs"]:
                params[kwarg] = (
                    kwargs.pop(kwarg, default) if default is not inspect.Parameter.empty else kwargs.pop(kwarg)
                )

            if var_kwargs := func_params.get("var_star_kwargs"):
                params[var_kwargs] = kwargs.copy()

            nonlocal result_type

            if result_type is None:
                result_type = get_shortcut_result_type(func)
            else:
                result_type = resolve_shortcut_result_type(result_type)

            return await executor(self, method_name, params, result_type)

        inner.__shortcut__ = Shortcut(  # type: ignore
            method_name=method_name,
            executor=executor,
            return_type=return_type,
            custom_params=custom_params or set(),
        )
        return inner  # type: ignore

    return wrapper


__all__ = ("Shortcut", "shortcut")
