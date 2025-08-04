import typing

_NOVALUE: typing.Any = object()


def private_func_name(func: typing.Callable[..., typing.Any], /) -> str:
    return "__" + func.__name__


class additional_property[T, R]:  # noqa: N801
    def __init__(self, func: typing.Callable[[T], R], /) -> None:
        self.func = func
        self.func_name = private_func_name(func)

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


class class_property[T]:  # noqa: N801
    def __init__(self, func: typing.Callable[..., T], /) -> None:
        self.func = func
        self.func_name = private_func_name(func)

    def __get__(self, instance: typing.Any | None, owner: type[typing.Any], /) -> T:
        return self.func(owner)


class class_cached_property[T]:  # noqa: N801
    def __init__(self, func: typing.Callable[..., T], /) -> None:
        self.func = func
        self.func_name = private_func_name(func)

    def __get__(self, instance: typing.Any | None, owner: type[typing.Any], /) -> T:
        value = getattr(owner, self.func_name, _NOVALUE)

        if value is _NOVALUE:
            value = self.func(owner)
            setattr(owner, self.func_name, value)

        return value


__all__ = ("additional_property", "class_cached_property", "class_property")
