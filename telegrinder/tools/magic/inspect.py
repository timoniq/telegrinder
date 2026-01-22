import sys


def get_frame_module_name() -> str:
    frame = sys._getframe()

    while frame:
        if frame.f_globals.get("__name__", "").startswith("telegrinder"):
            frame = frame.f_back
        else:
            break

    return "<module>" if frame is None else frame.f_globals.get("__name__", "<module>")


__all__ = ("get_frame_module_name",)
