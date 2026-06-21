import threading
import typing


class SingletonMeta(type):
    if not typing.TYPE_CHECKING:
        __instance = None
        __lock = threading.Lock()

        def __call__(cls, *args, **kwargs):
            if cls.__instance is None:
                with cls.__lock:
                    # Double-checked locking: the critical section spans an arbitrary
                    # constructor, so the GIL alone does not make check-then-create atomic.
                    if cls.__instance is None:
                        cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class Singleton(metaclass=SingletonMeta):
    pass


__all__ = ("Singleton", "SingletonMeta")
