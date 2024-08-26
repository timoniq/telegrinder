import dataclasses
import inspect
import typing
from functools import wraps

import typing_extensions
from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.model import Model, get_params

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])
Cute = typing.TypeVar("Cute", bound="BaseCute")
Update = typing_extensions.TypeVar("Update", bound=Model)
CtxAPI = typing_extensions.TypeVar("CtxAPI", bound=API, default=API)

Executor: typing.TypeAlias = typing.Callable[
    [Cute, str, dict[str, typing.Any]],
    typing.Awaitable[Result[typing.Any, typing.Any]],
]

if typing.TYPE_CHECKING:

    class BaseCute(Model, typing.Generic[Update, CtxAPI]):
        api: API

        @classmethod
        def from_update(cls, update: Update, bound_api: API) -> typing.Self: ...

        @property
        def ctx_api(self) -> CtxAPI: ...

        def to_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]:
            """
            :param exclude_fields: Cute model field names to exclude from the dictionary representation of this cute model.
            :return: A dictionary representation of this cute model.
            """

            ...

        def to_full_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]:
            """
            :param exclude_fields: Cute model field names to exclude from the dictionary representation of this cute model.
            :return: A dictionary representation of this model including all models, structs, custom types.
            """

            ...

else:
    from fntypes.co import Nothing, Some, Variative

    from telegrinder.msgspec_utils import Option, decoder
    from telegrinder.msgspec_utils import get_class_annotations as _get_class_annotations

    def _get_cute_from_generic(generic_args):
        for arg in generic_args:
            orig_arg = typing.get_origin(arg) or arg

            if not isinstance(orig_arg, type):
                continue
            if orig_arg in (Variative, Some, Option):
                return _get_cute_from_generic(typing.get_args(arg))
            if issubclass(arg, BaseCute):
                return arg

        return None

    def _get_cute_annotations(annotations):
        cute_annotations = {}

        for key, hint in annotations.items():
            if not isinstance(hint, type):
                if (cute := _get_cute_from_generic(typing.get_args(hint))) is not None:
                    cute_annotations[key] = cute

            elif issubclass(hint, BaseCute):
                cute_annotations[key] = hint

        return cute_annotations

    def _get_value(value):
        while isinstance(value, Variative | Some):
            if isinstance(value, Variative):
                value = value.v
            if isinstance(value, Some):
                value = value.value
        return value

    class BaseCute(typing.Generic[Update, CtxAPI]):
        def __init_subclass__(cls, *args, **kwargs):
            super().__init_subclass__(*args, **kwargs)

            if not cls.__bases__ or not issubclass(cls.__bases__[0], BaseCute):
                return

            cls.__is_solved_annotations__ = False
            cls.__cute_annotations__ = None

        @classmethod
        def from_update(cls, update, bound_api):
            if not cls.__is_solved_annotations__:
                cls.__is_solved_annotations__ = True
                cls.__annotations__ = _get_class_annotations(cls)

            if cls.__cute_annotations__ is None:
                cls.__cute_annotations__ = _get_cute_annotations(cls.__annotations__)

            return cls(
                **{
                    field: decoder.convert(
                        cls.__cute_annotations__[field].from_update(_get_value(value), bound_api=bound_api),
                        type=cls.__annotations__[field],
                    )
                    if field in cls.__cute_annotations__ and not isinstance(value, Nothing)
                    else value
                    for field, value in update.to_dict().items()
                },
                api=bound_api,
            )

        @property
        def ctx_api(self):
            return self.api

        def to_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return super().to_dict(exclude_fields={"api"} | exclude_fields)

        def to_full_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return super().to_full_dict(exclude_fields={"api"} | exclude_fields)


def compose_method_params(
    params: dict[str, typing.Any],
    update: Cute,
    *,
    default_params: set[str | tuple[str, str]] | None = None,
    validators: dict[str, typing.Callable[[Cute], bool]] | None = None,
) -> dict[str, typing.Any]:
    """Compose method `params` from `update` by `default_params` and `validators`.

    :param params: Method params.
    :param update: Update object.
    :param default_params: Default params. \
    (`str`) - Attribute name to be get from `update` if param is undefined. \
    (`tuple[str, str]`): tuple[0] - Parameter name to be set in `params`, \
    tuple[1] - attribute name to be get from `update`.
    :param validators: Validators mapping (`str, Callable`), key - `Parameter name` \
    for which the validator will be applied, value - `Validator`, if returned `True` \
    parameter will be set, otherwise will not.
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


def shortcut(
    method_name: str,
    *,
    executor: Executor[Cute] | None = None,
    custom_params: set[str] | None = None,
):
    def wrapper(func: F) -> F:
        @wraps(func)
        async def inner(
            self: Cute,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> typing.Any:
            if executor is None:
                return await func(self, *args, **kwargs)

            if not hasattr(func, "_signature_params"):
                setattr(
                    func,
                    "_signature_params",
                    {k: p for k, p in inspect.signature(func).parameters.items() if k != "self"},
                )

            signature_params: dict[str, inspect.Parameter] = getattr(func, "_signature_params")
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


@dataclasses.dataclass(slots=True, frozen=True)
class Shortcut:
    method_name: str
    executor: Executor | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set(), kw_only=True)


__all__ = ("BaseCute", "Shortcut", "compose_method_params", "shortcut")
