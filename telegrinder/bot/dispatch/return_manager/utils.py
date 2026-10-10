import types
from annotationlib import type_repr

import typing_extensions as typing


def _get_types(type_form: typing.TypeForm[typing.Any], /) -> tuple[typing.Any, ...]:
    while True:
        if isinstance(type_form, typing.TypeAliasType):
            type_form = type_form.__value__
            continue

        if isinstance(type_form, types.UnionType):
            return tuple(_get_types(arg) for arg in typing.get_args(type_form))

        if isinstance(type_form, types.GenericAlias):
            type_form = typing.get_origin(type_form)

        if isinstance(type_form, type):
            return (type_form,)

        # Unrecognized annotation (e.g. None, a forward-ref string, an instance): without this
        # the loop would spin forever making no progress.
        raise TypeError(f"Unsupported return type annotation: `{type_repr(type_form)}`")


__all__ = ("_get_types",)
