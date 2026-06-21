import types
import typing


def _get_types(x: typing.Any, /) -> type[typing.Any] | tuple[typing.Any, ...]:
    while True:
        if isinstance(x, types.UnionType | typing._UnionGenericAlias):  # type: ignore
            return tuple(_get_types(arg) for arg in typing.get_args(x))

        if isinstance(x, typing.TypeAliasType):
            x = x.__value__
            continue

        if isinstance(x, types.GenericAlias | typing._GenericAlias):  # type: ignore
            x = typing.get_origin(x)
            continue

        if isinstance(x, type):
            return x

        # Unrecognized annotation (e.g. None, a forward-ref string, an instance): without this
        # the loop would spin forever making no progress.
        raise TypeError(f"Unsupported return type annotation: {x!r}")


__all__ = ("_get_types",)
