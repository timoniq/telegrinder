import dataclasses
import inspect
import typing
from functools import wraps

from fntypes.result import Result

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model, get_params

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])
CuteT = typing.TypeVar("CuteT", bound="BaseCute")
UpdateT = typing.TypeVar("UpdateT", bound=Model)

Executor: typing.TypeAlias = typing.Callable[
    [CuteT, str, dict[str, typing.Any]],
    typing.Awaitable[Result[typing.Any, typing.Any]],
]

if typing.TYPE_CHECKING:

    class BaseCute(Model, typing.Generic[UpdateT]):
        api: ABCAPI

        @classmethod
        def from_update(cls, update: UpdateT, bound_api: ABCAPI) -> typing.Self: ...

        @property
        def ctx_api(self) -> API: ...

else:

    class BaseCute(typing.Generic[UpdateT]):
        @classmethod
        def from_update(cls, update, bound_api):
            return cls(**update.to_dict(), api=bound_api)

        @property
        def ctx_api(self):
            assert isinstance(self.api, API)
            return self.api

        def to_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return super().to_dict(exclude_fields={"api"} | exclude_fields)


def compose_method_params(
    params: dict[str, typing.Any],
    update: CuteT,
    *,
    default_params: set[str | tuple[str, str]] | None = None,
    validators: dict[str, typing.Callable[[CuteT], bool]] | None = None,
) -> dict[str, typing.Any]:
    """Compose method `params` from `update` by `default_params` and `validators`.
    
    :param params: Method params.
    :param update: Update object.
    :param default_params: Default params. \
    type (`str`) - Attribute name to be taken from `update` if param undefined. \
    type (`tuple[str, str]`) - tuple[0] Parameter name to be set in `params`, \
    tuple[1] attribute name to be taken from `update`.
    :param validators: Validators mapping (`str, Callable`), key - `Parameter name` \
    for which the validator will be applied, value - `Validator`, if returned `True` \
    parameter will be set, otherwise will not be set.
    :return: Composed params.
    """

    default_params = default_params or set()
    validators = validators or {}

    for param in default_params:
        param_name = param if isinstance(param, str) else param[0]
        if param_name not in params:
            if param_name in validators and not validators[param_name](update):
                continue
            params[param_name] = getattr(update, param if isinstance(param, str) else param[1])

    return params


# NOTE: implement parser on ast for methods decorated this decorator
# to support updates to the schema Bot API.
def shortcut(
    method_name: str,
    *,
    executor: Executor[CuteT] | None = None,
    custom_params: set[str] | None = None,
):
    def wrapper(func: F) -> F:
        @wraps(func)
        async def inner(
            self: CuteT,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> typing.Any:
            if executor is None:
                return await func(self, *args, **kwargs)
            signature_params = {
                k: p for k, p in inspect.signature(func).parameters.items() if k != "self"
            }
            params: dict[str, typing.Any] = {}
            index = 0

            for k, p in signature_params.items():
                if p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY) and len(args) > index:
                    params[k] = args[index]
                    index += 1
                    continue
                if p.kind in (p.VAR_KEYWORD, p.VAR_POSITIONAL):
                    params[k] = kwargs.copy() if p.kind is p.VAR_KEYWORD else args[index:]
                    continue
                params[k] = kwargs.pop(k, p.default) if p.default is not p.empty else kwargs.pop(k)

            return await executor(self, method_name, get_params(params))

        inner.__shortcut__ = Shortcut(  # type: ignore
            method_name=method_name,
            executor=executor,
            custom_params=custom_params or set(),
        )
        return inner  # type: ignore

    return wrapper


@dataclasses.dataclass
class Shortcut:
    method_name: str
    _: dataclasses.KW_ONLY
    executor: Executor | None = dataclasses.field(default=None)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set())


__all__ = ("BaseCute", "Shortcut", "compose_method_params", "shortcut")
