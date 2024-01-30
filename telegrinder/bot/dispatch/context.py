import enum
import typing

from telegrinder.types import Update

Key: typing.TypeAlias = str | enum.Enum
AnyValue: typing.TypeAlias = typing.Any


@typing.dataclass_transform(kw_only_default=True, order_default=True)
class Context(dict[str, AnyValue]):
    """Context class for rules and middlewares.
    ```
    class MyRule(ABCRule[T]):
        adapter: ABCAdapter[Update, T] = RawUpdateAdapter()

        async def check(self, event: T, ctx: Context) -> bool:
            ctx.set("value", (await event.ctx_api.get_me()).unwrap())
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
    
    def __setitem__(self, __key: Key, __value: AnyValue) -> None:
        super().__setitem__(self.key_to_str(__key), __value)
    
    def __getitem__(self, __key: Key) -> AnyValue:
        return super().__getitem__(self.key_to_str(__key))
    
    def __delitem__(self, __key: Key) -> None:
        super().__delattr__(self.key_to_str(__key))

    def __setattr__(self, __name: str, __value: AnyValue) -> None:
        self.__setitem__(__name, __value)
    
    def __getattr__(self, __name: str) -> AnyValue:
        return self.__getitem__(__name)
    
    def __delattr__(self, __name: str) -> None:
        return self.__delitem__(__name)

    @staticmethod
    def key_to_str(key: Key) -> str:
        return key if isinstance(key, str) else str(key.value)
    
    def copy(self) -> typing.Self:
        return self.__class__(**self)

    def set(self, key: Key, value: AnyValue) -> None:
        self[self.key_to_str(key)] = value
    
    def get(self, key: Key) -> AnyValue:
        return self[self.key_to_str(key)]
    
    def delete(self, key: Key) -> None:
        del self[self.key_to_str(key)]


__all__ = ("Context",)
