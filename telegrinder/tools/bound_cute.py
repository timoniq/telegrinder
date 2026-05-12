import inspect
import sys
import typing
from functools import cache

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute


class BoundCuteMeta(type):
    cute_type: typing.ClassVar[type[BaseCute] | str]
    cute_module: typing.ClassVar[str | None]

    def __instancecheck__(cls, instance: typing.Any, /) -> bool:
        return isinstance(instance, typing.cast("typing.Any", cls).resolve_cute_type())


class BoundCuteMixin(metaclass=BoundCuteMeta):
    cute_type: typing.ClassVar[type[BaseCute] | str]
    cute_module: typing.ClassVar[str | None] = None

    @classmethod
    @cache
    def resolve_cute_type(cls) -> type[BaseCute]:
        if not isinstance(cls.cute_type, str):
            return cls.cute_type

        module = sys.modules.get(cls.cute_module or "")

        if module is None or not isinstance(cute_type := getattr(module, cls.cute_type, None), type):
            raise TypeError(f"Cannot resolve cute type {cls.cute_type!r}.")

        cls.cute_type = cute_type
        return cute_type

    def __class_getitem__(cls, cute: typing.Any, /) -> typing.Any:
        frame = inspect.currentframe()
        module = cls.__module__

        try:
            if frame is not None and frame.f_back is not None:
                module = frame.f_back.f_globals.get("__name__", module)
        finally:
            del frame

        return type(
            "BoundCute",
            (BoundCute,),  # type: ignore
            {"__module__": module, "cute_type": cute, "cute_module": module},
        )


if typing.TYPE_CHECKING:
    type BoundCute[T: BaseCute] = T

else:

    class BoundCute(BoundCuteMixin):
        pass


__all__ = ("BoundCute",)
