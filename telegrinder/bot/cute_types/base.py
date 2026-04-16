from __future__ import annotations

import typing
from functools import cached_property

from kungfu.library import Some, Sum
from msgspec._utils import get_class_annotations
from msgspex import Option, encoder, struct_asdict
from msgspex.model import Model
from nodnod.error import NodeError

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.objects import Update

BOUND_API_KEY: typing.Final = "bound_api"
BOUND_UPDATE_KEY: typing.Final = "bound_update"


def compose_method_params[Cute: BaseCute](
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
            params[param_name] = getattr(update, param if isinstance(param, str) else param[1], None)

    return params


def get_cute_from_generic(generic_args: tuple[typing.Any, ...], /) -> typing.Any:
    for arg in generic_args:
        orig_arg = typing.get_origin(arg) or arg

        if not isinstance(orig_arg, type):
            continue

        if orig_arg in (Sum, Some, Option):
            return get_cute_from_generic(typing.get_args(arg))

        if issubclass(orig_arg, BaseCute):
            return arg

    return None


def get_cute_annotations(annotations: dict[str, typing.Any], /) -> dict[str, type[BaseCute]]:
    cute_annotations = {}

    for key, hint in annotations.items():
        if not isinstance(hint, type) and (cute := get_cute_from_generic(typing.get_args(hint))) is not None:
            cute_annotations[key] = cute

        elif isinstance(hint, type) and issubclass(hint, BaseCute):
            cute_annotations[key] = hint

    return cute_annotations


def maybe_wrapped(value: typing.Any, /) -> typing.Any:
    wrapped_value = None

    while isinstance(value, Sum | Some):
        wrapped_value = value

        if isinstance(value, Sum):
            value = value.v

        if isinstance(value, Some):
            value = value.value

    return wrapped_value if wrapped_value is not None else value


def wrap_value(value: typing.Any, type_: typing.Any, /) -> typing.Any:
    args = [type_]
    types = []

    while args:
        arg = args.pop(0)
        origin_arg = typing.get_origin(arg) or arg

        if issubclass(origin_arg, Sum | Option):  # type: ignore
            args.extend(typing.get_args(arg))
            types.append(Some if issubclass(origin_arg, Option) else arg)  # type: ignore

    result = value

    for t in types[::-1]:
        result = t(result)

    return result


def to_cute(
    cute_cls: type[BaseCute],
    field: str,
    value: typing.Any,
    bound_api: API,
) -> typing.Any:
    maybe_wrapped_value = maybe_wrapped(value)
    is_wrapped_value = isinstance(maybe_wrapped_value, Sum | Some)
    cute_annotations = cute_cls.__cute_annotations__

    if cute_annotations is None:
        cute_annotations = get_cute_annotations(get_class_annotations(cute_cls))

    cute = cute_annotations[field].from_update(
        maybe_wrapped_value._value if is_wrapped_value else maybe_wrapped_value,
        bound_api=bound_api,
    )
    return wrap_value(cute, cute_cls.__annotations__[field]) if is_wrapped_value else cute


class BaseCute[T: Model = typing.Any](Model):
    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        cls.__is_resolved_annotations__ = False
        cls.__cute_annotations__ = None
        super().__init_subclass__(*args, **kwargs)

    @classmethod
    def __compose__(cls, context: Context) -> typing.Any:
        update_cute = context.update_cute

        if type(update_cute) is cls:
            return update_cute

        if type(update_cute.incoming_update) is cls:
            return update_cute.incoming_update

        raise NodeError(f"Incoming update is not `{cls.__name__}`.")

    @classmethod
    def from_update(cls, update: Update, bound_api: API) -> typing.Self:
        if not cls.__is_resolved_annotations__:
            cls.__is_resolved_annotations__ = True
            cls.__annotations__ = get_class_annotations(cls)

        if cls.__cute_annotations__ is None:
            cls.__cute_annotations__ = get_cute_annotations(cls.__annotations__)

        cute: typing.Self = type(Model).model_initialize(  # type: ignore
            cls,
            **{
                field: to_cute(cls, field, value, bound_api) if field in cls.__cute_annotations__ else value
                for field, value in update.to_dict().items()
            },
        )
        return cute.bind(update, bound_api) if isinstance(update, Update) else cute._bind_api(bound_api)

    @cached_property
    def bound_api(self) -> API: ...

    @cached_property
    def bound_update(self) -> Update: ...

    @property
    def api(self) -> API:
        return self.bound_api

    def bind(self, update: Update, api: API) -> typing.Self:
        self._set_bounds_in_namespace({BOUND_UPDATE_KEY: update, BOUND_API_KEY: api})
        return self

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
        full: bool = False,
    ) -> dict[str, typing.Any]:
        return self._to_dict(
            "model_as_dict" if not full else "model_as_full_dict",
            exclude_fields=exclude_fields or set(),
            full=full,
        )

    def to_full_dict(self, *, exclude_fields: set[str] | None = None) -> dict[str, typing.Any]:
        return self.to_dict(exclude_fields=exclude_fields, full=True)

    def _to_dict(self, dct_name: str, exclude_fields: set[str], full: bool) -> dict[str, typing.Any]:
        if dct_name not in self.__dict__:
            dct = struct_asdict(self)
            self.__dict__[dct_name] = dct if not full else encoder.to_builtins(dct)  # type: ignore

        if not exclude_fields:
            return self.__dict__[dct_name]

        return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

    def _set_bounds_in_namespace(self, bounds: dict[str, typing.Any], /) -> None:
        cuties = [self]

        if isinstance(self, Update):
            cuties.append(self.incoming_update)

        for cute in cuties:
            for key, bound in bounds.items():
                cute.__dict__[key] = bound  # type: ignore

    def _bind_api(self, api: API) -> typing.Self:
        self._set_bounds_in_namespace({BOUND_API_KEY: api})
        return self


class BaseShortcuts[T: BaseCute = typing.Any]:
    @cached_property
    def cute(self) -> typing.Self:
        return self


__all__ = ("BaseCute", "BaseShortcuts", "compose_method_params", "shortcut")
