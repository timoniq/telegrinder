import types
import typing

import fntypes.co
import msgspec

if typing.TYPE_CHECKING:
    from datetime import datetime

    from fntypes.option import Option

    from telegrinder.tools.fullname import fullname
    from telegrinder.tools.magic import magic_bundle

    def get_class_annotations(obj: typing.Any, /) -> dict[str, typing.Any]: ...

    def get_type_hints(obj: typing.Any, /) -> dict[str, typing.Any]: ...

else:
    from datetime import datetime as dt

    from msgspec._utils import get_class_annotations, get_type_hints

    datetime = type("datetime", (dt,), {})

    class OptionMeta(type):
        def __instancecheck__(cls, __instance: typing.Any) -> bool:
            return isinstance(__instance, (fntypes.option.Some | fntypes.option.Nothing, msgspec.UnsetType))

    class Option[Value](metaclass=OptionMeta):
        pass

    def magic_bundle(*args, **kwargs):
        from telegrinder.tools.magic import magic_bundle

        return magic_bundle(*args, **kwargs)

    def fullname(*args, **kwargs):
        from telegrinder.tools.fullname import fullname

        return fullname(*args, **kwargs)


_COMMON_TYPES = frozenset((str, int, float, bool, None, fntypes.co.Variative))


def get_origin[T](t: type[T], /) -> type[T]:
    t_ = typing.get_origin(t) or t
    t_ = type(t_) if not isinstance(t_, type) else t_
    return typing.cast("type[T]", t_)


def is_common_type[T](t: T, /) -> typing.TypeGuard[type[T]]:
    if not isinstance(t, type):
        return False
    return t in _COMMON_TYPES or issubclass(t, msgspec.Struct) or hasattr(t, "__dataclass_fields__")


def struct_asdict(struct: msgspec.Struct, /) -> dict[str, typing.Any]:
    return {
        k: v
        for k, v in msgspec.structs.asdict(struct).items()
        if not isinstance(v, msgspec.UnsetType | types.NoneType | fntypes.option.Nothing)
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
    "Option",
    "datetime",
    "get_class_annotations",
    "get_origin",
    "get_type_hints",
    "is_common_type",
    "struct_asdict",
    "type_check",
)
