import builtins
import inspect
import os.path
import sys
import types
import typing

type RoutineMethodType = (
    types.MethodType | types.MethodDescriptorType | types.MethodWrapperType | types.BuiltinMethodType
)
type RoutineDescriptorType = types.MethodDescriptorType | types.GetSetDescriptorType

_BUILTINS: typing.Final[frozenset[typing.Any]] = frozenset(
    x for name in dir(builtins) if getattr((x := getattr(builtins, name)), "__module__", None) == "builtins"
)
_CACHE_KEY: typing.Final[str] = "__fullname_cache__"


def _is_builtin(obj: typing.Any, /) -> bool:
    return inspect.isbuiltin(obj) or obj in _BUILTINS


def _is_routine_method(obj: typing.Any, /) -> typing.TypeIs[RoutineMethodType]:
    return inspect.isbuiltin(obj) or inspect.ismethod(obj) or inspect.ismethodwrapper(obj)


def _is_routine_descriptor(obj: typing.Any, /) -> typing.TypeIs[RoutineDescriptorType]:
    return inspect.ismethoddescriptor(obj) or inspect.isgetsetdescriptor(obj)


def _module_name(module: types.ModuleType, /) -> str:
    if (mod_name := module.__name__) != "__main__":
        return mod_name

    mod_package = module.__package__ or ""
    mod_file = module.__file__
    if mod_file is None:
        return mod_package

    mod_fname = os.path.basename(mod_file).removesuffix(".py")
    return mod_package if mod_package in ("__init__", "__main__") else mod_fname


def fullname(obj: object, /) -> str:
    """The full name (`__module__.__name__`) of the object."""

    if isinstance(obj, staticmethod | classmethod):
        obj = obj.__func__

    elif (
        not inspect.isroutine(obj)
        and not inspect.isgetsetdescriptor(obj)
        and not isinstance(obj, type)
        and not inspect.ismodule(obj)
    ):
        obj = type(obj)

    if (name := fullname.__dict__.setdefault(_CACHE_KEY, dict()).get(obj)) is not None:
        return name

    if inspect.ismodule(obj):
        fullname.__dict__[_CACHE_KEY][obj] = name = _module_name(obj)
        return name

    qualname = obj.__qualname__
    orig_obj = obj

    if _is_routine_method(obj) or _is_routine_descriptor(obj):
        obj_cls = obj.__objclass__ if _is_routine_descriptor(obj) else obj.__self__
        obj = type(obj_cls) if not isinstance(obj_cls, type) else obj_cls

    module: str = getattr(orig_obj, "__module__", obj.__module__)
    if _is_builtin(obj) and module != builtins.__name__:
        module = builtins.__name__
    else:
        module = _module_name(sys.modules[module])

    fullname.__dict__[_CACHE_KEY][orig_obj] = name = ".".join((module, qualname))
    return name


__all__ = ("fullname",)
