import typing


class SingletonMeta(type):
    if not typing.TYPE_CHECKING:
        __instance = None

        def __call__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class Singleton(metaclass=SingletonMeta):
    pass


__all__ = ("Singleton", "SingletonMeta")
