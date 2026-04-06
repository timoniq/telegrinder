import typing

from telegrinder.msgspec_utils import decoder, encoder
from telegrinder.tools.fullname import fullname
from telegrinder.types.enums import DateTimeFormat


class DateTimeFormatSeq(tuple[DateTimeFormat, ...]):
    _string_format: str

    def __new__(cls, iterable: typing.Iterable[DateTimeFormat], s: str | None = None, /) -> typing.Self:
        instance = super().__new__(cls, iterable)
        instance._string_format = s if s else "".join(fmt.value for fmt in iterable)
        return instance

    def __str__(self) -> str:
        return self._string_format

    @property
    def string_format(self) -> str:
        return self._string_format


@decoder.add_dec_hook(DateTimeFormatSeq)
def decode_date_time_format_seq(t: type[DateTimeFormatSeq], value: typing.Any, /) -> DateTimeFormatSeq:
    if isinstance(value, t):
        return value

    if isinstance(value, str):
        return DateTimeFormatSeq((DateTimeFormat(char) for char in value), value)

    if isinstance(value, typing.Iterable):
        return DateTimeFormatSeq(decoder.convert(value, type=tuple[DateTimeFormat, ...]))

    raise TypeError(
        f"Expected `{fullname(t)}` or iterable of `{fullname(str)} | {fullname(DateTimeFormat)}`, "
        f"got `{fullname(value)}`",
    )


@encoder.add_enc_hook(DateTimeFormatSeq)
def encode_date_time_format_seq(obj: DateTimeFormatSeq, /) -> str:
    return obj.string_format


__all__ = ("DateTimeFormatSeq",)
