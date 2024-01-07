import enum
import typing

Key: typing.TypeAlias = str | enum.Enum
Value: typing.TypeAlias = typing.Any


@typing.dataclass_transform(kw_only_default=True)
class Context(dict[Key, Value]):
    """Context class for rules and middlewares.
    ```
    class MyRule(ABCRule[T]):
        adapter: ABCAdapter[Update, T] = RawUpdateAdapter()

        async def check(self, event: T, ctx: Context) -> bool:
            ctx.set("value", (await event.ctx_api.get_me()).unwrap())
            return True
    ```
    """

    __setattr__ = dict.__setitem__  # type: ignore
    __getattr__ = dict.__getitem__  # type: ignore
    __delattr__ = dict.__delitem__  # type: ignore

    def __init__(self, **kwargs: Value) -> None:
        cls_vars = vars(self.__class__)
        defaults = {}
        for k in self.__class__.__annotations__:
            if k in cls_vars:
                defaults[k] = cls_vars[k]
                delattr(self.__class__, k)
        dict.__init__(self, **defaults | kwargs)
    
    def copy(self) -> typing.Self:
        return self.__class__(**self)

    def set(self, key: Key, value: Value) -> None:
        self[key] = value
    
    def get(self, key: Key) -> Value:
        return self[key]
    
    def delete(self, key: Key) -> None:
        del self[key]
