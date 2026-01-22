import typing

if typing.TYPE_CHECKING:
    from kungfu.library.monad.option import Option
else:
    import kungfu.library
    import msgspec

    class OptionMeta(type):
        def __instancecheck__(cls, __instance):
            return isinstance(__instance, (kungfu.library.Some | kungfu.library.Nothing, msgspec.UnsetType))

    class Option[Value](metaclass=OptionMeta):
        pass


__all__ = ("Option",)
