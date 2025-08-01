import types
import typing

import fntypes.library
import msgspec

if typing.TYPE_CHECKING:
    from telegrinder.tools.fullname import fullname
    from telegrinder.tools.magic.function import bundle

    def get_class_annotations(obj: typing.Any, /) -> dict[str, typing.Any]: ...

    def get_type_hints(obj: typing.Any, /) -> dict[str, typing.Any]: ...

else:
    from msgspec._utils import get_class_annotations, get_type_hints

    def bundle(*args, **kwargs):
        from telegrinder.tools.magic.function import bundle

        return bundle(*args, **kwargs)

    def fullname(*args, **kwargs):
        from telegrinder.tools.fullname import fullname

        return fullname(*args, **kwargs)


_NOTHING = fntypes.library.Nothing()
_COMMON_TYPES = frozenset((str, int, float, bool, None, fntypes.library.Variative))


def get_origin[T](t: T, /) -> type[T]:
    t_ = typing.get_origin(t) or t
    t_ = type(t_) if not isinstance(t_, type) else t_
    return typing.cast("type[T]", t_)


def is_common_type[T](t: T, /) -> typing.TypeGuard[type[T]]:
    if not isinstance(t, type):
        return False
    return t in _COMMON_TYPES or issubclass(t, msgspec.Struct) or hasattr(t, "__dataclass_fields__")


def struct_asdict(
    struct: msgspec.Struct,
    /,
    *,
    exclude_unset: bool = True,
    unset_as_nothing: bool = False,
) -> dict[str, typing.Any]:
    return {
        k: v if not unset_as_nothing else _NOTHING if v is msgspec.UNSET else v
        for k, v in msgspec.structs.asdict(struct).items()
        if not (exclude_unset and isinstance(v, msgspec.UnsetType | types.NoneType | fntypes.library.Nothing))
    }


def type_check(obj: typing.Any, t: typing.Any) -> bool:
    return (
        isinstance(obj, t)
        if isinstance(t, type) and issubclass(t, msgspec.Struct)
        else type(obj) in t
        if isinstance(t, tuple)
        else type(obj) is t
    )


__all__ = (
    "get_class_annotations",
    "get_origin",
    "get_type_hints",
    "is_common_type",
    "struct_asdict",
    "type_check",
)
