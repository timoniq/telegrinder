import typing

from fntypes.option import Some
from fntypes.variative import Variative

from telegrinder.model import Model
from telegrinder.msgspec_utils import Nothing

T = typing.TypeVar("T", bound="Source")


@typing.runtime_checkable
class Source(typing.Protocol): ...


def unwrap_value(value: typing.Any) -> typing.Any | None:
    if value in (Nothing, None):
        return None
    if isinstance(value, Some):
        return unwrap_value(value.unwrap())
    if isinstance(value, Variative):
        return unwrap_value(value.v)
    return value


def get_by_sources(model: Model, sources: type[T] | list[type[T]]) -> typing.Any | None:
    """
    For example:

    ```python
    @typing.runtime_checkable
    class HasFrom(Source, typing.Protocol):
        from_: User
    

    @typing.runtime_checkable
    class HasUser(Source, typing.Protocol):
        user: User
    

    class Message(Model):
        from_: User
    

    class MessageReactionUpdated(Model):
        user: User
    

    get_by_sources(Message(...), [HasFrom, HasUser])  # User(...)
    get_by_sources(Message(...), HasUser)  # None

    get_by_sources(MessageReactionUpdated(), [HasFrom, HasUser])  # User(...)
    get_by_sources(Message(...), HasFrom)  # None
    ```
    """

    sources = [sources] if not isinstance(sources, list) else sources
    for source in sources:
        if isinstance(model, source):
            return next(
                (
                    unwrap_value(getattr(model, field))
                    for field in model.__struct_fields__
                    if field in typing.get_type_hints(source)
                ),
                None,
            )

        values = filter(None, [
            getattr(model, field, None)
            for field in model.__struct_fields__
        ])
        for value in values:
            value = unwrap_value(value)
            if isinstance(value, Model) and (result := get_by_sources(value, sources)) is not None:
                return result
            for t in typing.get_type_hints(source).values():
                if isinstance(value, t):
                    return value
    
    return None


__all__ = ("Source", "unwrap_value", "get_by_sources")
