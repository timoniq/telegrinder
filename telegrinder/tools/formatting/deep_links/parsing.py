import types
import typing
from collections import OrderedDict
from datetime import timedelta
from urllib.parse import urlencode

from telegrinder.tools.magic import get_annotations

type DeepLinkFunction[**P] = typing.Callable[P, str]
type NoValue = types.EllipsisType

Parameter = typing.Annotated

NO_VALUE: typing.Final[NoValue] = typing.cast("NoValue", ...)


def get_query_params(
    func: DeepLinkFunction[...],
    kwargs: dict[str, typing.Any],
    order_params: set[str] | None = None,
) -> dict[str, typing.Any]:
    annotations = get_annotations(func)
    params = OrderedDict()
    param_names = (
        [*order_params, *(p for p in annotations if p not in order_params)] if order_params else annotations
    )

    for param_name in param_names:
        annotation = annotations[param_name]
        if param_name in kwargs:
            value = kwargs[param_name]
            if typing.get_origin(annotation) is Parameter:
                param_name, validator = get_parameter_metadata(annotation)
                value = validator(value) if validator is not None else value

            params[param_name] = value

    return params


def parse_query_params(
    params: dict[str, typing.Any],
    no_value_params: set[str] | None = None,
    /,
) -> tuple[set[str], dict[str, typing.Any]]:
    no_value_params = no_value_params or set()
    params_: dict[str, typing.Any] = {}

    for key, value in params.items():
        if value in (False, None):
            continue

        if value in (True, NO_VALUE):
            no_value_params.add(key)
            continue
        if isinstance(value, timedelta):
            value = int(value.total_seconds())

        params_[key] = value

    return (no_value_params, params_)


def get_parameter_metadata(
    parameter: typing.Any,
) -> tuple[str, typing.Callable[[typing.Any], typing.Any] | None]:
    meta: tuple[typing.Any, ...] = getattr(parameter, "__metadata__")
    return meta if len(meta) == 2 else (meta[0], None)


def parse_deep_link(
    *,
    link: str,
    params: dict[str, typing.Any],
    no_value_params: set[str] | None = None,
) -> str:
    no_value_params, params = parse_query_params(params, no_value_params)
    query = urlencode(params, encoding="UTF-8") + ("&" if no_value_params else "") + "&".join(no_value_params)
    return f"{link}?{query}"


__all__ = (
    "NO_VALUE",
    "NoValue",
    "Parameter",
    "get_parameter_metadata",
    "get_query_params",
    "parse_deep_link",
    "parse_query_params",
)
