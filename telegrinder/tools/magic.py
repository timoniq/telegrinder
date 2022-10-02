import inspect
import types
import typing

AnyMock = type("Any", (object,), {"__str__": lambda _: "Any"})


class VarUnset(BaseException):
    def __init__(self, name: str, t: typing.Any, handler: types.FunctionType):
        self.name = name
        self.t = t
        self.handler = handler

    def __repr__(self):
        return (
            f"Handler {self.handler.__name__} requires variable {self.name} of type {self.t} "
            "which was not set in the context"
        )

    def __str__(self):
        return self.__repr__()


def resolve_arg_names(func: types.FunctionType) -> typing.Tuple[str, ...]:
    return func.__code__.co_varnames[1 : func.__code__.co_argcount]


def get_default_args(func: types.FunctionType) -> typing.Dict[str, typing.Any]:
    fspec = inspect.getfullargspec(func)
    return dict(zip(fspec.args[::-1], (fspec.defaults or ())[::-1]))


def magic_bundle(
    handler: types.FunctionType, kw: typing.Dict[str, typing.Any]
) -> typing.Dict[str, typing.Any]:
    args = get_default_args(handler) | kw
    arg_names = resolve_arg_names(handler)
    hints = typing.get_type_hints(handler)
    kw_new = {}
    for name in arg_names:
        if name not in args:
            raise VarUnset(name, hints.get(name, AnyMock).__name__, handler)
        kw_new[name] = args[name]
    return kw_new
