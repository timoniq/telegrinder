import dataclasses
import inspect
import typing
from functools import wraps

import typing_extensions
from fntypes.result import Result

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model, get_params

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])
Cute = typing.TypeVar("Cute", bound="BaseCute")
Update = typing_extensions.TypeVar("Update", bound=Model)
CtxAPI = typing_extensions.TypeVar("CtxAPI", bound=ABCAPI, default=API)

Executor: typing.TypeAlias = typing.Callable[
    [Cute, str, dict[str, typing.Any]],
    typing.Awaitable[Result[typing.Any, typing.Any]],
]

if typing.TYPE_CHECKING:

    class BaseCute(Model, typing.Generic[Update, CtxAPI]):
        api: ABCAPI

        @classmethod
        def from_update(cls, update: Update, bound_api: ABCAPI) -> typing.Self: ...

        @property
        def ctx_api(self) -> CtxAPI: ...

else:
    from fntypes import Some, Variative
    from msgspec._utils import get_class_annotations

    from telegrinder.msgspec_utils import Option

    DEFAULT_API_CLASS = API
    UPDATED_ANNOTATIONS_KEY = "__updated_annotations__"

    def unwrap_value(value):
        origin = typing.get_origin(value) or value
        if isinstance(origin, Variative):
            return unwrap_value(value.v)
        if isinstance(origin, Some):
            return unwrap_value(value.unwrap())
        return value

    def wrap_cute_model(cute_model, hint):
        orig_hint = typing.get_origin(hint) or hint
        if orig_hint not in (Option, Variative):
            return cute_model

        for h in typing.get_args(hint):
            cute = wrap_cute_model(cute_model, h)

        orig_hint = typing.get_origin(hint) or hint
        if orig_hint is Option:
            cute_model = Some(cute_model)
        elif orig_hint is Variative:
            cute_model = hint(cute_model)

        return cute_model

    def get_ctx_api_class(cute_class):
        """Get ctx_api class from generic.

        >>> my_cute = MyMessageCute[Message, MyAPI](...)
        >>> get_ctx_api_class(type(my_cute))
        >>> "<class '__main__.MyAPI'>"
        >>> message_cute = MessageCute(...)
        >>> get_ctx_api_class(type(message_cute))
        >>> "<class 'telegrinder.api.api.API'>"
        """

        for base in cute_class.__dict__.get("__orig_bases__", ()):
            if issubclass(typing.get_origin(base) or base, BaseCute):
                for generic_type in typing.get_args(base):
                    if issubclass(typing.get_origin(generic_type) or generic_type, ABCAPI):
                        return generic_type
        return DEFAULT_API_CLASS

    def has_cute_annotation(model_type, annotation):
        origin_annotation = typing.get_origin(annotation) or annotation

        if isinstance(origin_annotation, type) and issubclass(origin_annotation, model_type):
            return True
        return any(has_cute_annotation(model_type, ann) for ann in typing.get_args(annotation))

    def get_cute_type(model_type, annotation, container_cuties):
        """Get cute type from container cuties
        if it is annotated and it is a subclass of a `model_type`."""

        if not has_cute_annotation(model_type, annotation):
            return None

        for cute in container_cuties:
            if issubclass(cute, model_type):
                return cute

        return None

    class BaseCute(typing.Generic[Update, CtxAPI]):
        def __init_subclass__(cls, *args, **kwargs):
            setattr(cls, UPDATED_ANNOTATIONS_KEY, False)  # Dunder variable with state for update annotations

            super().__init_subclass__(
                *args, **kwargs
            )  # Call msgspec.Struct.__init_subclass__() for configuration struct

            if not cls.__bases__ or not issubclass(cls.__bases__[0], BaseCute):
                return

            if not hasattr(BaseCute, "container_cuties"):
                setattr(
                    BaseCute, "container_cuties", []
                )  # Create container with all cute types which inherit BaseCute class
            getattr(BaseCute, "container_cuties").append(cls)  # Append current cute type to container

        @classmethod
        def from_update(cls, update, bound_api):
            if not getattr(cls, UPDATED_ANNOTATIONS_KEY, False):
                setattr(cls, UPDATED_ANNOTATIONS_KEY, True)
                setattr(
                    cls, "__annotations__", get_class_annotations(cls)
                )  # Solve forward refs and update annotations

            container_cuties = BaseCute.container_cuties
            update_dct = {}

            for k, v in update.to_dict().items():
                value = unwrap_value(v)
                if (
                    k in cls.__annotations__
                    and (cute := get_cute_type(value.__class__, cls.__annotations__[k], container_cuties))
                    is not None
                ):
                    update_dct[k] = wrap_cute_model(
                        cute.from_update(value, bound_api=bound_api), cls.__annotations__[k]
                    )
                else:
                    update_dct[k] = v

            return cls(**update_dct, api=bound_api)

        @property
        def ctx_api(self):
            ctx_api_class = get_ctx_api_class(self.__class__)
            assert isinstance(
                self.api, get_ctx_api_class(self.__class__)
            ), f"Bound API of type {self.api.__class__.__name__!r} is incompatible with {ctx_api_class.__name__!r}."
            return self.api

        def to_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return super().to_dict(exclude_fields={"api"} | exclude_fields)


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


# NOTE: implement parser on ast for methods decorated this decorator
# to support updates to the schema Bot API.
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
            signature_params = {k: p for k, p in inspect.signature(func).parameters.items() if k != "self"}
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
    executor: Executor | None = dataclasses.field(default=None, kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set(), kw_only=True)


__all__ = ("BaseCute", "Shortcut", "compose_method_params", "shortcut")
