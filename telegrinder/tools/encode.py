import msgspec
from msgspex.custom_types import datetime
from msgspex.encoder import encoder


@encoder.add_enc_hook(datetime)
async def datetime_to_int_timestamp_hook(obj: datetime, /) -> int:
    try:
        return int(obj.timestamp())
    except Exception as exc:
        raise msgspec.ValidationError(exc)


__all__ = ("datetime_to_int_timestamp_hook",)
