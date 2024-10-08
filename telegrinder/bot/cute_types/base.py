import dataclasses
import inspect
import typing
from collections import OrderedDict
from functools import wraps

import msgspec
import typing_extensions
from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.model import Model, get_params
from telegrinder.tools.magic import get_func_parameters

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
    import msgspec
    from fntypes.co import Nothing, Some, Variative

    from telegrinder.msgspec_utils import Option, decoder, encoder
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

        def _to_dict(self, dct_name, exclude_fields, full):
            if dct_name not in self.__dict__:
                self.__dict__[dct_name] = (
                    msgspec.structs.asdict(self)
                    if not full
                    else encoder.to_builtins(
                        {
                            k: field.to_dict(exclude_fields=exclude_fields)
                            if isinstance(field := _get_value(getattr(self, k)), BaseCute)
                            else field
                            for k in self.__struct_fields__
                            if k not in exclude_fields
                        },
                        order="deterministic",
                    )
                )

            if not exclude_fields:
                return self.__dict__[dct_name]

            return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

        def to_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return self._to_dict("model_as_dict", exclude_fields={"api"} | exclude_fields, full=False)

        def to_full_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return self._to_dict("model_as_full_dict", exclude_fields={"api"} | exclude_fields, full=True)


def compose_method_params(
    params: dict[str, typing.Any],
    update: Cute,
    *,
    default_params: set[str | tuple[str, str]] | None = None,
    validators: dict[str, typing.Callable[[Cute], bool]] | None = None,
) -> dict[str, typing.Any]:
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
    """Decorate a cute method as a shortcut."""

    def wrapper(func: F) -> F:
        @wraps(func)
        async def inner(
            self: Cute,
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
                    kwargs.pop(kwarg, default)
                    if default is not inspect.Parameter.empty
                    else kwargs.pop(kwarg)
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


@dataclasses.dataclass(slots=True, frozen=True)
class Shortcut(typing.Generic[Cute]):
    method_name: str
    executor: Executor[Cute] | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set(), kw_only=True)


__all__ = ("BaseCute", "Shortcut", "compose_method_params", "shortcut")
