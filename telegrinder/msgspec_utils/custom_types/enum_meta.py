import enum
import typing


class BaseEnumMeta(enum.EnumMeta, type):
    if typing.TYPE_CHECKING:

        class BaseEnumMeta(enum.Enum):  # noqa
            NOT_SUPPORTED = enum.auto()

        NOT_SUPPORTED: typing.Literal[BaseEnumMeta.NOT_SUPPORTED]

    else:

        @staticmethod
        def _member_missing(cls, value):
            from telegrinder.modules import logger

            logger.warning(
                "Unsupported value {!r} for enum of type {!r}. Probably teleginder needs to be "
                "updated to support the latest version of Telegram Bot API.",
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
            classdict["NOT_SUPPORTED"] = "NOT_SUPPORTED" if any(x in bases for x in (str, enum.StrEnum)) else -1
            classdict["_missing_"] = classmethod(BaseEnumMeta._member_missing)
            new_type = super().__new__(metacls, cls, bases, classdict, boundary=boundary, _simple=_simple, **kwds)
            return new_type


__all__ = ("BaseEnumMeta",)
