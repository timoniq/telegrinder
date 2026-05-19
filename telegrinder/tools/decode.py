import typing
from datetime import timezone

from msgspex.custom_types import datetime
from msgspex.decoder import decoder
from msgspex.tools import fullname

from telegrinder.tools.bound_cute import BoundCute, BoundCuteMixin
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.base import BaseCute


@decoder.add_dec_hook(datetime)
def int_timestamp_to_datetime_hook(_: type[datetime], obj: typing.Any) -> datetime:
    if isinstance(obj, int):
        return datetime.fromtimestamp(timestamp=obj, tz=timezone.utc)
    raise TypeError(f"Excepted `builtins.int` for decode to `datetime.datetime`, got `{fullname(obj)}`")


@decoder.add_abstract_dec_hook(BoundCute)
def bound_cute_hook(
    bound_cute: BoundCuteMixin,
    obj: dict[str, typing.Any],
    *,
    ctx_api: API | None = None,
) -> BaseCute:
    cute = decoder.convert(
        obj,
        type=bound_cute.resolve_cute_type(),
        context=dict(ctx_api=ctx_api) if ctx_api is not None else None,
    )

    if isinstance(cute, Update):
        getattr(cute.bind_update(cute).incoming_update, "bind_update")(cute)

    return cute.bind_api(ctx_api) if ctx_api is not None else cute


__all__ = ("int_timestamp_to_datetime_hook",)
