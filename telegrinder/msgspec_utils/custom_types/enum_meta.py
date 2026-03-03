import enum
import math
import sys
import typing

from telegrinder.modules import logger

NOT_SUPPORTED: typing.Final = "NOT_SUPPORTED"
ENUM_FRIENDS: typing.Final = (str, int, float)
NOT_SUPPORTED_VALUES: typing.Final = {
    str: NOT_SUPPORTED,
    int: sys.maxsize,
    float: math.inf,
}


def _is_friend(bases: tuple[type[typing.Any], ...], /) -> bool:
    return any(friend in bases for friend in ENUM_FRIENDS)


class BaseEnumMeta(enum.EnumMeta, type):
    if typing.TYPE_CHECKING:

        class _BaseEnumMeta(enum.Enum):  # noqa
            NOT_SUPPORTED = enum.auto()

        NOT_SUPPORTED: typing.Literal[_BaseEnumMeta.NOT_SUPPORTED]

    else:

        @staticmethod
        def _member_missing(cls, value):
            logger.warning(
                "Unsupported value {!r} for enum of type {}. Probably telegrinder needs "
                "to be updated to support the latest version of Telegram Bot API.",
                value,
                cls,
            )
            return cls._member_map_["NOT_SUPPORTED"]

        def __new__(
            metacls,
            cls,
            bases,
            classdict,
            *,
            boundary=None,
            _simple=False,
            **kwds,
        ):
            if _is_friend(bases):
                classdict["NOT_SUPPORTED"] = next(
                    (value for base, value in NOT_SUPPORTED_VALUES.items() if base in bases),
                    NOT_SUPPORTED,
                )

            classdict["_missing_"] = classmethod(BaseEnumMeta._member_missing)
            return super().__new__(metacls, cls, bases, classdict, boundary=boundary, _simple=_simple, **kwds)


__all__ = ("BaseEnumMeta",)
