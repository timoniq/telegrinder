import msgspec
from msgspex.custom_types import datetime, timedelta
from msgspex.encoder import encoder


@encoder.add_enc_hook(datetime)
def datetime_to_int_timestamp_hook(obj: datetime, /) -> int:
    try:
        return int(obj.timestamp())
    except Exception as exc:
        raise msgspec.ValidationError(exc)


@encoder.add_enc_hook(timedelta)
def timedelta_to_int_timedelta(obj: timedelta) -> int:
    try:
        return int(obj.total_seconds())
    except Exception as exc:
        raise msgspec.ValidationError(exc)


__all__ = ("datetime_to_int_timestamp_hook", "timedelta_to_int_timedelta")
