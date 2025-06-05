import datetime as dt
import typing

from telegrinder.msgspec_utils.abc import SupportsCast


class datetime(dt.datetime, SupportsCast):  # noqa: N801  # type: ignore
    @classmethod
    def cast(cls, obj: dt.datetime) -> typing.Self:
        return cls.fromtimestamp(timestamp=obj.timestamp(), tz=obj.tzinfo)


class timedelta(dt.timedelta, SupportsCast):  # noqa: N801  # type: ignore
    @classmethod
    def cast(cls, obj: dt.timedelta) -> typing.Self:
        return cls(seconds=obj.total_seconds())


if typing.TYPE_CHECKING:
    datetime: typing.TypeAlias = dt.datetime
    timedelta: typing.TypeAlias = dt.timedelta


__all__ = ("datetime", "timedelta")
