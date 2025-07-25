import dataclasses
import sys
import types
import typing as _typing
from functools import cached_property

import typing_extensions as typing
from fntypes.library.monad.option import Nothing, Option, Some

from telegrinder.tools.global_context.global_context import GlobalContext, ctx_var

type TypeParameter = typing.Union[
    typing.TypeVar,
    typing.TypeVarTuple,
    typing.ParamSpec,
    _typing.TypeVar,
    _typing.TypeVarTuple,
    _typing.ParamSpec,
]
type TypeParameters = tuple[TypeParameter, ...]
type SupportsAnnotations = type[typing.Any] | types.ModuleType | typing.Callable[..., typing.Any]

_CACHED_ANNOTATIONS: typing.Final[GlobalContext] = GlobalContext(
    "cached_annotations",
    annotations=ctx_var(default_factory=dict, const=True),
)


def _cache_annotations(obj: SupportsAnnotations, annotations: dict[str, typing.Any], /) -> None:
    _CACHED_ANNOTATIONS.annotations[obj] = annotations


def _get_cached_annotations(obj: SupportsAnnotations, /) -> dict[str, typing.Any] | None:
    return _CACHED_ANNOTATIONS.annotations.get(obj)


@dataclasses.dataclass
class Annotations:
    obj: SupportsAnnotations

    @cached_property
    def forward_ref_parameters(self) -> dict[str, typing.Any]:
        parameters = dict[str, typing.Any](
            is_argument=False,
            is_class=False,
            module=None,
        )

        if isinstance(self.obj, type):
            parameters["is_class"] = True
            parameters["module"] = (
                sys.modules[module] if (module := getattr(self.obj, "__module__", None)) is not None else None
            )
        elif isinstance(self.obj, types.ModuleType):
            parameters["module"] = self.obj
        elif callable(self.obj):
            parameters["is_argument"] = True

        return parameters

    @cached_property
    def generic_parameters(self) -> Option[dict[TypeParameter, typing.Any]]:
        return get_generic_parameters(self.obj)

    @classmethod
    def from_obj(cls, obj: typing.Any, /) -> typing.Self:
        if not isinstance(obj, type | types.ModuleType | typing.Callable):
            obj = type(obj)

        return cls(obj)

    @typing.overload
    def get(
        self,
        *,
        ignore_failed_evals: bool = True,
        allow_return_type: bool = False,
        cache: bool = False,
    ) -> dict[str, typing.Any | typing.ForwardRef]: ...

    @typing.overload
    def get(
        self,
        *,
        exclude_forward_refs: typing.Literal[True],
        ignore_failed_evals: bool = True,
        allow_return_type: bool = False,
        cache: bool = False,
    ) -> dict[str, typing.Any]: ...

    def get(
        self,
        *,
        exclude_forward_refs: bool = False,
        ignore_failed_evals: bool = True,
        allow_return_type: bool = True,
        cache: bool = False,
    ) -> dict[str, typing.Any]:
        if (cached_annotations := _get_cached_annotations(self.obj)) is not None:
            return cached_annotations

        annotations = dict[str, typing.Any]()
        for name, annotation in typing.get_annotations(
            obj=self.obj,
            format=typing.Format.FORWARDREF,
        ).items():
            if isinstance(annotation, str):
                annotation = typing.ForwardRef(annotation, **self.forward_ref_parameters)

            if not isinstance(annotation, typing.ForwardRef):
                annotations[name] = annotation
                continue

            try:
                value = typing.evaluate_forward_ref(
                    forward_ref=annotation,
                    owner=self.obj,
                    format=typing.Format.VALUE,
                )
            except NameError:
                if not ignore_failed_evals:
                    raise

                value = annotation

            if isinstance(value, typing.ForwardRef) and exclude_forward_refs:
                continue

            annotations[name] = value

        if not allow_return_type:
            annotations.pop("return", None)

        if cache:
            _cache_annotations(self.obj, annotations)

        return annotations


def get_generic_parameters(obj: typing.Any, /) -> Option[dict[TypeParameter, typing.Any]]:
    origin_obj = _typing.get_origin(obj)
    args = _typing.get_args(obj)
    parameters: TypeParameters = getattr(origin_obj or obj, "__parameters__")

    if not parameters:
        return Nothing()

    index = 0
    generic_alias_args = dict[TypeParameter, _typing.Any]()

    for parameter in parameters:
        if isinstance(parameter, _typing.TypeVarTuple):
            stop_index = len(args) - index
            generic_alias_args[parameter] = args[index:stop_index]
            index = stop_index
            continue

        arg = args[index] if index < len(args) else None
        generic_alias_args[parameter] = arg
        index += 1

    return Some(generic_alias_args)


__all__ = ("Annotations", "get_generic_parameters")
