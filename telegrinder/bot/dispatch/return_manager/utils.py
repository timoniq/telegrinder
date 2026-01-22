import types
import typing


def _get_types(x: typing.Any, /) -> type[typing.Any] | tuple[typing.Any, ...]:
    while True:
        if isinstance(x, types.UnionType | typing._UnionGenericAlias):  # type: ignore
            return tuple(_get_types(x) for x in typing.get_args(x))

        if isinstance(x, typing.TypeAliasType):
            x = x.__value__

        if isinstance(x, types.GenericAlias | typing._GenericAlias):  # type: ignore
            x = typing.get_origin(x)

        if isinstance(x, type):
            return x


__all__ = ("_get_types",)
