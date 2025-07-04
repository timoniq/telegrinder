from __future__ import annotations

import dataclasses
import inspect
import typing
from collections import OrderedDict
from functools import wraps

from fntypes.result import Result

from telegrinder.tools.magic.function import get_func_parameters
from telegrinder.types.methods_utils import get_params

type Executor[T] = typing.Callable[
    [T, str, dict[str, typing.Any]],
    typing.Awaitable[Result[typing.Any, APIError]],
]
type CuteMethod[T, **P, R] = typing.Callable[
    typing.Concatenate[T, P],
    typing.Awaitable[Result[R, APIError]],
]

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError


class ShortcutMethod[T, **P, R](typing.Protocol):
    __name__: str
    __shortcut__: Shortcut[T]

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Result[R, APIError]: ...


@dataclasses.dataclass(slots=True, frozen=True)
class Shortcut[T]:
    method_name: str
    executor: Executor[T] | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set[str](), kw_only=True)


@typing.overload
def shortcut[T, **P, R](
    method_name: str,
    /,
    *,
    custom_params: set[str] = ...,
) -> typing.Callable[[CuteMethod[T, P, R]], ShortcutMethod[T, P, R]]: ...


@typing.overload
def shortcut[T, **P, R](
    method_name: str,
    /,
    *,
    executor: Executor[T],
    custom_params: set[str] = ...,
) -> typing.Callable[[CuteMethod[T, P, R]], ShortcutMethod[T, P, R]]: ...


def shortcut[T, **P, R](
    method_name: str,
    /,
    *,
    executor: Executor[T] | None = None,
    custom_params: set[str] | None = None,
) -> typing.Callable[[CuteMethod[T, P, R]], ShortcutMethod[T, P, R]]:
    """Decorate a cute method as a shortcut."""

    def wrapper(func: CuteMethod[T, P, R]) -> ShortcutMethod[T, P, R]:
        @wraps(func)
        async def inner(
            self: T,
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

            return await executor(self, method_name, get_params(params))

        inner.__shortcut__ = Shortcut(  # type: ignore
            method_name=method_name,
            executor=executor,
            custom_params=custom_params or set(),
        )
        return inner  # type: ignore

    return wrapper


__all__ = ("Shortcut", "shortcut")
