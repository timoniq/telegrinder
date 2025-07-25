import typing

_NOVALUE: typing.Any = object()


class additional_property[T, R]:  # noqa: N801
    def __init__(self, func: typing.Callable[[T], R], /) -> None:
        self.func = func

    @property
    def func_name(self) -> str:
        return "_" + self.func.__name__

    def __set__(self, instance: T, value: typing.Any, /) -> None:
        instance.__dict__[self.func_name] = value

    def __get__(self, instance: T | None, owner: type[T], /) -> typing.Any:
        if instance is None:
            raise AttributeError("Cannot access additional property from class.")

        value = instance.__dict__.get(self.func_name, _NOVALUE)
        if value is _NOVALUE:
            value = self.func(instance)
            instance.__dict__[self.func_name] = value

        return value

    def __delete__(self, instance: T, /) -> None:
        instance.__dict__.pop(self.func_name, None)


__all__ = ("additional_property",)
