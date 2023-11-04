import dataclasses
import string
import typing
from contextlib import suppress

from telegrinder.tools.parse_mode import ParseMode, get_mention_link

TAG_FORMAT = "<{tag}{data}>{content}</{tag}>"
QUOT_MARK = '"'


@dataclasses.dataclass(repr=False)
class Mention:
    string: str
    user_id: int

    def __post_init__(self) -> None:
        self.string = escape(self.string)


@dataclasses.dataclass(repr=False)
class Link:
    href: str
    string: str | None = None

    def __post_init__(self) -> None:
        self.href = escape(self.href)
        self.string = escape(self.string or self.href)


@dataclasses.dataclass(repr=False)
class PreCode:
    string: str
    lang: str | None = None

    def __post_init__(self) -> None:
        self.string = escape(self.string)


@dataclasses.dataclass(repr=False)
class TgEmoji:
    string: str
    emoji_id: int

    def __post_init__(self) -> None:
        self.string = escape(self.string)


class StringFormatter(string.Formatter):
    """String formatter, using substitutions from args and kwargs.
    The substitutions are identified by braces ('{' and '}') with
    specifiers: `bold`, `italic`, etc.
    """

    __formats__ = (
        "bold",
        "italic",
        "strike",
        "spoiler",
        "underline",
        "code_inline",
    )
    __special_formats__ = {
        TgEmoji: "tg_emoji",
        PreCode: "pre_code",
        Mention: "mention",
        Link: "link",
    }

    def is_html_format(self, value: typing.Any, fmt: str) -> str:
        if not fmt:
            raise ValueError("Formats union should be: format+format.")
        if fmt not in self.__formats__:
            raise ValueError(
                "Unknown format {!r} for object of type {!r}.".format(
                    fmt,
                    type(value).__name__,
                )
            )
        return fmt

    def is_spec_html_formatter(
        self,
        value: typing.Any,
    ) -> typing.TypeGuard[TgEmoji | PreCode | Mention | Link]:
        return type(value) in self.__special_formats__

    def get_spec_formatter(
        self,
        value: typing.Any,
    ) -> typing.Callable[..., "TagFormat"]:
        return globals()[self.__special_formats__[type(value)]]

    def check_formats(self, value: typing.Any, fmts: list[str]) -> "TagFormat":
        if self.is_spec_html_formatter(value):
            value = value.string

        current_format = globals()[fmts.pop(0)](
            str(value)
            if isinstance(value, TagFormat)
            else escape(FormatString(value) if not isinstance(value, str) else value)
        )
        for fmt in fmts:
            current_format = globals()[fmt](current_format)

        return (
            TagFormat(
                current_format,
                tag=value.tag,
                **value.data,
            )
            if isinstance(value, TagFormat)
            else current_format
        )

    def format_field(self, value: typing.Any, fmt: str) -> "HTMLFormatter":
        with suppress(ValueError):
            return HTMLFormatter(
                format(
                    value.formatting()
                    if isinstance(value, TagFormat)
                    else self.get_spec_formatter(value)(**value.__dict__).formatting()
                    if self.is_spec_html_formatter(value)
                    else value,
                    fmt,
                )
            )
        return self.format_raw_value(value, fmt)

    def format_raw_value(self, value: typing.Any, fmt: str) -> "HTMLFormatter":
        fmts = list(map(lambda fmt: self.is_html_format(value, fmt), fmt.split("+")))
        tag_format = self.check_formats(value, fmts)

        if self.is_spec_html_formatter(value):
            value.string = tag_format
            tag_format = self.get_spec_formatter(value)(**dataclasses.asdict(value))

        return tag_format.formatting()

    def format(self, __string: str, *args: object, **kwargs: object) -> "HTMLFormatter":
        return HTMLFormatter(super().format(__string, *args, **kwargs))


class FormatString(str):
    string_formatter = StringFormatter()

    def __new__(cls, string: str) -> typing.Self:
        if isinstance(string, TagFormat):
            return super().__new__(cls, string.formatting())
        return super().__new__(cls, string)

    def __add__(self, value: str) -> "HTMLFormatter":
        return HTMLFormatter(
            str.__add__(
                escape(self),
                value.formatting() if isinstance(value, TagFormat) else escape(value),
            )
        )

    def __radd__(self, value: str) -> "HTMLFormatter":
        """Return value+self."""
        return HTMLFormatter(FormatString.__add__(FormatString(value), self).as_str())

    def as_str(self) -> str:
        """Return self as a standart string."""
        return self.__str__()

    def format(self, *args: object, **kwargs: object) -> "HTMLFormatter":
        return self.string_formatter.format(self, *args, **kwargs)


class EscapedString(FormatString):
    @property
    def former_string(self) -> str:
        return self.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")


class TagFormat(FormatString):
    tag: str
    data: dict[str, typing.Any]

    def __new__(
        cls,
        string: str,
        *,
        tag: str,
        **data: typing.Any,
    ) -> typing.Self:
        if isinstance(string, TagFormat):
            string = string.formatting()
        elif not isinstance(
            string,
            (
                EscapedString,
                HTMLFormatter,
            ),
        ):
            string = escape(string)
        obj = super().__new__(cls, string)
        obj.tag = tag
        obj.data = data
        return obj

    def get_tag_data(self) -> str:
        return "".join(f" {k}={v}" for k, v in self.data.items())

    def formatting(self) -> "HTMLFormatter":
        return HTMLFormatter(
            TAG_FORMAT.format(
                tag=self.tag,
                data=self.get_tag_data(),
                content=self,
            )
        )


class HTMLFormatter(FormatString):
    """
    >>> HTMLFormatter(bold("Hello, World"))
    '<b>Hello, World</b>'
    HTMLFormatter("Hi, {name:italic}").format(name="Max")
    'Hi, <i>Max</i>'
    """

    PARSE_MODE = ParseMode.HTML


def escape(string: str) -> EscapedString:
    if isinstance(string, EscapedString | HTMLFormatter):
        return EscapedString(string)
    return EscapedString(
        string.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
    )


def bold(string: str) -> TagFormat:
    return TagFormat(string, tag="b")


def italic(string: str) -> TagFormat:
    return TagFormat(string, tag="i")


def underline(string: str) -> TagFormat:
    return TagFormat(string, tag="u")


def strike(string: str) -> TagFormat:
    return TagFormat(string, tag="s")


def spoiler(string: str) -> TagFormat:
    return TagFormat(string, tag="tg-spoiler")


def link(href: str, string: str | None = None) -> TagFormat:
    href = escape(href)
    return TagFormat(
        string or href,
        tag="a",
        href=QUOT_MARK + href + QUOT_MARK,
    )


def mention(string: str, user_id: int) -> TagFormat:
    return link(get_mention_link(user_id), string)


def pre_code(string: str, lang: str | None = None) -> TagFormat:
    if lang is None:
        return TagFormat(string, tag="pre")
    return pre_code(TagFormat(string, tag="code", **{"class": f"language-{lang}"}))


def code_inline(string: str) -> TagFormat:
    return TagFormat(string, tag="code")


def tg_emoji(string: str, emoji_id: int) -> TagFormat:
    return TagFormat(string, tag="tg-emoji", **{"emoji-id": emoji_id})
