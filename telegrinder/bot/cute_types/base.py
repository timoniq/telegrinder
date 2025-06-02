import typing

import msgspec

from telegrinder.model import Model, is_none
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

        def to_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]:
            """:param exclude_fields: Cute model field names to exclude from the dictionary representation of this cute model.
            :return: A dictionary representation of this cute model.
            """
            ...

        def to_full_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]:
            """:param exclude_fields: Cute model field names to exclude from the dictionary representation of this cute model.
            :return: A dictionary representation of this model including all models, structs, custom types.
            """
            ...

else:
    import types

    import msgspec
    from fntypes.co import Nothing, Some, Variative

    from telegrinder.msgspec_utils import Option, decoder, encoder, struct_asdict
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

    def _validate_value(value, /):
        while isinstance(value, Variative | Some):
            if isinstance(value, Variative):
                value = value.v
            if isinstance(value, Some):
                value = value.value
        return value

    class BaseCute[T]:
        def __init_subclass__(cls, *args, **kwargs):
            super().__init_subclass__(*args, **kwargs)

            if not cls.__bases__ or BaseCute not in cls.__bases__:
                return

            cls.__is_solved_annotations__ = False
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
            if not cls.__is_solved_annotations__:
                cls.__is_solved_annotations__ = True
                cls.__annotations__ = _get_class_annotations(cls)

            if cls.__cute_annotations__ is None:
                cls.__cute_annotations__ = _get_cute_annotations(cls.__annotations__)

            cute = cls(
                **{
                    field: decoder.convert(
                        cls.__cute_annotations__[field].from_update(_validate_value(value), bound_api=bound_api),
                        type=cls.__annotations__[field],
                    )
                    if field in cls.__cute_annotations__
                    and not isinstance(value, Nothing | msgspec.UnsetType | types.NoneType)
                    else value
                    for field, value in update.to_dict().items()
                },
            )._set_bound_api(api=bound_api)
            return cute.bind_raw_update(update) if isinstance(update, Update) else cute

        @property
        def api(self):
            return self.__dict__[BOUND_API_KEY]

        @property
        def raw_update(self):
            assert RAW_UPDATE_BIND_KEY in self.__dict__, (
                f"Cute model `{type(self).__name__}` has no bind `Update` object."
            )
            return self.__dict__[RAW_UPDATE_BIND_KEY]

        @property
        def ctx_api(self):
            return self.api

        def bind_raw_update(self, raw_update, /):
            self.__dict__[RAW_UPDATE_BIND_KEY] = raw_update
            if isinstance(cute := getattr(self, "incoming_update", None), BaseCute):
                cute.bind_raw_update(raw_update)
            return self

        def _set_bound_api(self, api):
            self.__dict__[BOUND_API_KEY] = api
            return self

        def _to_dict(self, dct_name, exclude_fields, full):
            if dct_name not in self.__dict__:
                self.__dict__[dct_name] = (
                    struct_asdict(self)
                    if not full
                    else encoder.to_builtins(
                        {
                            k: field.to_dict(exclude_fields=exclude_fields)
                            if isinstance(field, BaseCute)
                            else field
                            for k in self.__struct_fields__
                            if k not in exclude_fields
                            and not isinstance(field := _validate_value(getattr(self, k)), msgspec.UnsetType)
                            and not is_none(field)
                        },
                        order="deterministic",
                    )
                )

            if not exclude_fields:
                return self.__dict__[dct_name]

            return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

        def to_dict(self, *, exclude_fields=None, full=False):
            exclude_fields = exclude_fields or set()
            return self._to_dict("model_as_dict", exclude_fields={"api"} | exclude_fields, full=full)

        def to_full_dict(self, *, exclude_fields=None):
            return self.to_dict(exclude_fields=exclude_fields, full=True)


__all__ = ("BaseCute", "compose_method_params", "shortcut")
