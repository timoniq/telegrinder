import typing
from datetime import timezone

from msgspex.custom_types import datetime
from msgspex.decoder import decoder
from msgspex.tools import fullname


@decoder.add_dec_hook(datetime)
def int_timestamp_to_datetime_hook(_: type[datetime], obj: typing.Any) -> datetime:
    if isinstance(obj, int):
        return datetime.fromtimestamp(timestamp=obj, tz=timezone.utc)
    raise TypeError(f"Excepted `builtins.int` for decode to `datetime.datetime`, got `{fullname(obj)}`")


__all__ = ("int_timestamp_to_datetime_hook",)
