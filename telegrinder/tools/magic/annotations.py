import dataclasses
import inspect
import sys
import types
import typing as _typing
from functools import cached_property

import typing_extensions as typing
from fntypes.option import Nothing, Option, Some
from fntypes.result import Error, Ok, Result

from telegrinder.tools.fullname import fullname

type TypeParameter = typing.Union[
    typing.TypeVar,
    typing.TypeVarTuple,
    typing.ParamSpec,
    _typing.TypeVar,
    _typing.TypeVarTuple,
    _typing.ParamSpec,
]
type TypeParameters = tuple[TypeParameter, ...]


@dataclasses.dataclass(frozen=True)
class AnnotationsEvaluator:
    obj: typing.Any

    @cached_property
    def obj_dicts(self) -> tuple[dict[str, typing.Any], dict[str, typing.Any]]:
        return self._get_localns_and_globalns()

    @property
    def localns(self) -> dict[str, typing.Any]:
        return self.obj_dicts[0].copy()

    @property
    def globalns(self) -> dict[str, typing.Any]:
        return self.obj_dicts[1].copy()

    def evaluate(self, *, ignore_name_errors: bool = False) -> Result[typing.Mapping[str, typing.Any], str]:
        return self._evaluate(ignore_name_errors=ignore_name_errors)

    @staticmethod
    def evaluate_annotation(
        annotation: typing.Any,
        /,
        *,
        ignore_name_errors: bool,
        type_params: TypeParameters,
        localns: dict[str, typing.Any],
        globalns: dict[str, typing.Any],
    ) -> typing.Any:
        annotation = _typing._type_convert(annotation)  # type: ignore

        try:
            return _typing._eval_type(  # type: ignore
                annotation,
                globalns,
                localns,
                type_params,
            )
        except NameError as exception:
            if ignore_name_errors:
                return annotation
            raise exception

    def get_type_parameters(self, /) -> TypeParameters:
        params = ()

        if hasattr(self.obj, "__parameters__"):
            params = self.obj.__parameters__
        elif hasattr(self.obj, "__type_params__"):
            params = self.obj.__type_params__

        return params

    def _evaluate(self, *, ignore_name_errors: bool = False) -> Result[dict[str, typing.Any], str]:
        if not hasattr(self.obj, "__annotations__"):
            return Error(f"`{fullname(self.obj)}` has no `__annotations__`.")

        annotations = getattr(self.obj, "__annotations__")
        if not isinstance(annotations, typing.Mapping):
            return Error(f"`{fullname(self.obj)}.__annotations__ = {annotations!r}` is not a mapping.")

        type_params = self.get_type_parameters()
        return Ok(
            {
                name: self.evaluate_annotation(
                    annotation,
                    ignore_name_errors=ignore_name_errors,
                    type_params=type_params,
                    localns=self.localns,
                    globalns=self.globalns,
                )
                for name, annotation in annotations.items()
                if name != "return"
            }
        )

    def _get_module(self) -> types.ModuleType | None:
        if isinstance(self.obj, types.ModuleType):
            return self.obj

        if hasattr(self.obj, "__module__"):
            return sys.modules.get(self.obj.__module__, None)

        return None

    def _get_localns_and_globalns(self) -> tuple[dict[str, typing.Any], dict[str, typing.Any]]:
        if inspect.isfunction(self.obj):
            return dict(self.obj.__dict__), dict(self.obj.__globals__ or {})

        if isinstance(self.obj, types.ModuleType):
            ls = gs = dict(self.obj.__dict__ or {})
            return ls, gs

        module = self._get_module()
        return (
            dict(getattr(self.obj, "__dict__", {})),
            {} if module is None else dict(getattr(module, "__dict__", {})),
        )


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


__all__ = ("AnnotationsEvaluator", "get_generic_parameters")
