import os
import sys
import types


def get_module_name(module: types.ModuleType, /) -> str:
    if (mod_name := module.__name__) != "__main__":
        return mod_name

    mod_package = module.__package__ or ""
    mod_file = module.__file__
    if mod_file is None:
        return mod_package

    mod_fname = os.path.basename(mod_file).removesuffix(".py")
    return mod_package if mod_package in ("__init__", "__main__") else mod_fname


def get_frame_module_name() -> str:
    frame = sys._getframe()

    while frame:
        if frame.f_globals.get("__name__", "").startswith("telegrinder"):
            frame = frame.f_back
        else:
            break

    if frame is None or "__name__" not in frame.f_globals:
        return "<module>"

    module = sys.modules.get(frame.f_globals["__name__"])
    return get_module_name(module) if module is not None else "<module>"


__all__ = ("get_frame_module_name", "get_module_name")
