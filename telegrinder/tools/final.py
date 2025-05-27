import typing

from telegrinder.tools.fullname import fullname


class Final:
    if not typing.TYPE_CHECKING:

        def __new__(cls, *args, **kwargs):
            if cls is Final:
                raise TypeError("Class Final cannot be instantiate.")
            return super().__new__(cls, *args, **kwargs)

    @typing.final
    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        for base in cls.__bases__:
            if base is not Final and issubclass(base, Final):
                raise TypeError(f"Final class `{fullname(base)}` cannot be subclassed.")


__all__ = ("Final",)
