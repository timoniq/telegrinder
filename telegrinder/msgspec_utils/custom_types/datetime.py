import datetime as dt
import typing

from telegrinder.msgspec_utils.abc import SupportsCast


class _datetime(dt.datetime, SupportsCast):  # noqa: N801
    @classmethod
    def cast(cls, obj: dt.datetime) -> typing.Self:
        return cls.fromtimestamp(timestamp=obj.timestamp(), tz=obj.tzinfo)


class _timedelta(dt.timedelta, SupportsCast):  # noqa: N801
    @classmethod
    def cast(cls, obj: dt.timedelta) -> typing.Self:
        return cls(seconds=obj.total_seconds())


if typing.TYPE_CHECKING:
    datetime: typing.TypeAlias = dt.datetime
    timedelta: typing.TypeAlias = dt.timedelta
else:
    datetime = _datetime
    timedelta = _timedelta


__all__ = ("datetime", "timedelta")
