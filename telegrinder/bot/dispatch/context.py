import enum
import typing
from reprlib import recursive_repr

from telegrinder.types import Update

T = typing.TypeVar("T")

Key: typing.TypeAlias = str | enum.Enum
AnyValue: typing.TypeAlias = typing.Any


class Context(dict[str, AnyValue]):
    """Context class like dict & dotdict.

    For example:
    ```python
    class MyRule(ABCRule[T]):
        async def check(self, event: T, ctx: Context) -> bool:
            ctx.me = (await event.ctx_api.get_me()).unwrap()
            ctx["items"] = [1, 2, 3]
            return True
    ```
    """

    raw_update: Update

    def __init__(self, **kwargs: AnyValue) -> None:
        cls_vars = vars(self.__class__)
        defaults = {}

        for k in self.__class__.__annotations__:
            if k in cls_vars:
                defaults[k] = cls_vars[k]
                delattr(self.__class__, k)

        dict.__init__(self, **defaults | kwargs)

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, ", ".join(f"{k}={v!r}" for k, v in self.items()))

    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        dict.__setitem__(self, self.key_to_str(__key), __value)

    def __getitem__(self, __key: Key) -> AnyValue:
        return dict.__getitem__(self, self.key_to_str(__key))

    def __delitem__(self, __key: Key) -> None:
        dict.__delitem__(self, self.key_to_str(__key))

    def __setattr__(self, __name: str, __value: AnyValue) -> None:
        self.__setitem__(__name, __value)

    def __getattr__(self, __name: str) -> AnyValue:
        return self.__getitem__(__name)

    def __delattr__(self, __name: str) -> None:
        self.__delitem__(__name)

    @staticmethod
    def key_to_str(key: Key) -> str:
        return key if isinstance(key, str) else str(key.value)

    def copy(self) -> typing.Self:
        return self.__class__(**self)

    def set(self, key: Key, value: AnyValue) -> None:
        self[key] = value

    def get(self, key: Key, default: T | None = None) -> T | AnyValue:
        return dict.get(self, key, default)

    def get_or_set(self, key: Key, default: T) -> T:
        if key not in self:
            self.set(key, default)
        return self.get(key)

    def delete(self, key: Key) -> None:
        del self[key]


__all__ = ("Context",)
