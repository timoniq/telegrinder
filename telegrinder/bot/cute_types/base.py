import typing

from telegrinder.model import Model
from telegrinder.tools.magic.shortcut import shortcut


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
            params[param_name] = getattr(update, param if isinstance(param, str) else param[1])

    return params


if typing.TYPE_CHECKING:
    from fntypes.option import Option

    from telegrinder.api.api import API
    from telegrinder.node.base import Node
    from telegrinder.types.objects import Update

    class BaseCute[T: Model](Model):
        api: API

        @classmethod
        def as_node(cls) -> type[Node]: ...

        @classmethod
        def from_update(cls, update: T, bound_api: API) -> typing.Self: ...

        @property
        def ctx_api(self) -> API: ...

        @property
        def raw_update(self) -> Update: ...

        def bind_raw_update(self, raw_update: Update, /) -> typing.Self: ...

        def get_raw_update(self) -> Option[Update]: ...

        def to_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]: ...

        def to_full_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]: ...

else:
    from fntypes.co import Some, Variative
    from fntypes.misc import from_optional

    from telegrinder.msgspec_utils import Option, encoder, struct_asdict
    from telegrinder.msgspec_utils import get_class_annotations as _get_class_annotations
    from telegrinder.types.objects import Update

    BOUND_API_KEY = "bound_api"
    RAW_UPDATE_BIND_KEY = "raw_update_bind"

    def _get_cute_from_generic(generic_args, /):
        for arg in generic_args:
            orig_arg = typing.get_origin(arg) or arg

            if not isinstance(orig_arg, type):
                continue
            if orig_arg in (Variative, Some, Option):
                return _get_cute_from_generic(typing.get_args(arg))
            if issubclass(orig_arg, BaseCute):
                return arg

        return None

    def _get_cute_annotations(annotations, /):
        cute_annotations = {}

        for key, hint in annotations.items():
            if not isinstance(hint, type):
                if (cute := _get_cute_from_generic(typing.get_args(hint))) is not None:
                    cute_annotations[key] = cute

            elif issubclass(hint, BaseCute):
                cute_annotations[key] = hint

        return cute_annotations

    def _maybe_wrapped(value, /):
        wrapped_value = None

        while isinstance(value, Variative | Some):
            wrapped_value = value

            if isinstance(value, Variative):
                value = value.v

            if isinstance(value, Some):
                value = value.value

        return wrapped_value if wrapped_value is not None else value

    def _wrap_value(value, type_):
        args = [type_]
        types = []

        while args:
            arg = args.pop(0)
            origin_arg = typing.get_origin(arg) or arg
            if issubclass(origin_arg, Variative | Option):
                args.extend(typing.get_args(arg))
                types.append(Some if issubclass(origin_arg, Option) else arg)

        result = value
        for t in types[::-1]:
            result = t(result)
        return result

    def _to_cute(cls, field, value, bound_api):
        maybe_wrapped_value = _maybe_wrapped(value)
        is_wrapped_value = isinstance(maybe_wrapped_value, Variative | Some)
        cute = cls.__cute_annotations__[field].from_update(
            maybe_wrapped_value._value if is_wrapped_value else maybe_wrapped_value,
            bound_api=bound_api,
        )
        return _wrap_value(cute, cls.__annotations__[field]) if is_wrapped_value else cute

    class BaseCute[T]:
        def __init_subclass__(cls, *args, **kwargs):
            cls.__is_resolved_annotations__ = False
            cls.__cute_annotations__ = None
            cls.__event_node__ = None

        @classmethod
        def as_node(cls):
            if cls.__event_node__ is None:
                from telegrinder.node.event import EventNode

                cls.__event_node__ = EventNode[cls]

            return cls.__event_node__

        @classmethod
        def from_update(cls, update, bound_api):
            if not cls.__is_resolved_annotations__:
                cls.__is_resolved_annotations__ = True
                cls.__annotations__ = _get_class_annotations(cls)

            if cls.__cute_annotations__ is None:
                cls.__cute_annotations__ = _get_cute_annotations(cls.__annotations__)

            cute = cls(
                **{
                    field: _to_cute(cls, field, value, bound_api) if field in cls.__cute_annotations__ else value
                    for field, value in update.to_dict().items()
                },
            )._set_bound_api(api=bound_api)
            return cute.bind_raw_update(update) if isinstance(update, Update) else cute

        @property
        def api(self):
            return self.__dict__[BOUND_API_KEY]

        @property
        def raw_update(self):
            return self.get_raw_update().expect(
                ValueError(f"Cute model `{type(self).__name__}` has no bind `Update` object."),
            )

        @property
        def ctx_api(self):
            return self.api

        def get_raw_update(self):
            return from_optional(self.__dict__.get(RAW_UPDATE_BIND_KEY))

        def bind_raw_update(self, raw_update, /):
            cuties = [self]

            if isinstance(self, Update) and isinstance(cute := self.incoming_update, BaseCute):
                cuties.append(cute)

            for cute in cuties:
                cute.__dict__[RAW_UPDATE_BIND_KEY] = raw_update

            return self

        def _set_bound_api(self, api):
            self.__dict__[BOUND_API_KEY] = api
            return self

        def _to_dict(self, dct_name, exclude_fields, full):
            if dct_name not in self.__dict__:
                dct = struct_asdict(self)
                self.__dict__[dct_name] = dct if not full else encoder.to_builtins(dct, order="deterministic")

            if not exclude_fields:
                return self.__dict__[dct_name]

            return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

        def to_dict(self, *, exclude_fields=None, full=False):
            return self._to_dict(
                "model_as_dict" if not full else "model_as_full_dict",
                exclude_fields=exclude_fields or set(),
                full=full,
            )

        def to_full_dict(self, *, exclude_fields=None):
            return self.to_dict(exclude_fields=exclude_fields, full=True)


__all__ = ("BaseCute", "compose_method_params", "shortcut")
