import abc

from telegrinder.tools.singleton.singleton import SingletonMeta


class ABCSingletonMeta(abc.ABCMeta, SingletonMeta):
    pass


class ABCSingleton(metaclass=ABCSingletonMeta):
    pass


__all__ = ("ABCSingleton", "ABCSingletonMeta")
