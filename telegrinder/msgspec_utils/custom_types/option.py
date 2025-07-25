import typing

if typing.TYPE_CHECKING:
    from fntypes.library.monad.option import Option
else:
    import fntypes.library
    import msgspec

    class OptionMeta(type):
        def __instancecheck__(cls, __instance):
            return isinstance(__instance, (fntypes.library.Some | fntypes.library.Nothing, msgspec.UnsetType))

    class Option[Value](metaclass=OptionMeta):
        pass


__all__ = ("Option",)
