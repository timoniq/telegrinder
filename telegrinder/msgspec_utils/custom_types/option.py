import typing

if typing.TYPE_CHECKING:
    from fntypes.option import Option
else:
    import fntypes
    import msgspec

    class OptionMeta(type):
        def __instancecheck__(cls, __instance):
            return isinstance(__instance, (fntypes.option.Some | fntypes.option.Nothing, msgspec.UnsetType))

    class Option[Value](metaclass=OptionMeta):
        pass


__all__ = ("Option",)
