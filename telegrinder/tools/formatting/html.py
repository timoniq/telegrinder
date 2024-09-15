import html
import string
import typing
from contextlib import suppress

from telegrinder.tools.parse_mode import ParseMode
from telegrinder.types.enums import ProgrammingLanguage

from .links import (
    get_channel_boost_link,
    get_invite_chat_link,
    get_mention_link,
    get_resolve_domain_link,
    get_start_bot_link,
    get_start_group_link,
)
from .spec_html_formats import SpecialFormat, is_spec_format

TAG_FORMAT = "<{tag}{data}>{content}</{tag}>"
QUOT_MARK = '"'


class StringFormatterProto(typing.Protocol):
    def format_field(self, value: typing.Any, fmt: str) -> "HTMLFormatter": ...

    def format(self, __string: str, *args: object, **kwargs: object) -> "HTMLFormatter": ...


class StringFormatter(string.Formatter):
    """String formatter, using substitutions from args and kwargs.
    The substitutions are identified by braces ('{' and '}') with
    specifiers: `bold`, `italic`, etc.
    """

    __formats__: typing.ClassVar[tuple[str, ...]] = (
        "blockquote",
        "bold",
        "code_inline",
        "italic",
        "spoiler",
        "strike",
        "underline",
    )

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

    def get_spec_formatter(self, value: SpecialFormat) -> typing.Callable[..., "TagFormat"]:
        return globals()[value.__formatter_name__]

    def check_formats(self, value: typing.Any, fmts: list[str]) -> "TagFormat":
        if is_spec_format(value):
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
                    (
                        value.formatting()
                        if isinstance(value, TagFormat)
                        else (
                            self.get_spec_formatter(value)(**value.__dict__).formatting()
                            if is_spec_format(value)
                            else value
                        )
                    ),
                    fmt,
                )
            )
        return self.format_raw_value(value, fmt)

    def format_raw_value(self, value: typing.Any, fmt: str) -> "HTMLFormatter":
        fmts = list(map(lambda fmt: self.is_html_format(value, fmt), fmt.split("+")))
        tag_format = self.check_formats(value, fmts)

        if is_spec_format(value):
            value.string = tag_format
            tag_format = self.get_spec_formatter(value)(**value.__dict__)

        return tag_format.formatting()

    def format(self, __string: str, *args: object, **kwargs: object) -> "HTMLFormatter":
        return HTMLFormatter(super().format(__string, *args, **kwargs))


class FormatString(str):
    STRING_FORMATTER: StringFormatterProto = StringFormatter()

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
        return self.STRING_FORMATTER.format(self, *args, **kwargs)


class EscapedString(FormatString):
    @property
    def former_string(self) -> str:
        return html.unescape(self)


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
    return EscapedString(html.escape(string, quote=False))


def block_quote(string: str) -> TagFormat:
    return TagFormat(string, tag="blockquote")


def bold(string: str) -> TagFormat:
    return TagFormat(string, tag="b")


def channel_boost_link(channel_id: str | int, string: str | None = None):
    return link(get_channel_boost_link(channel_id), string)


def code_inline(string: str) -> TagFormat:
    return TagFormat(string, tag="code")


def italic(string: str) -> TagFormat:
    return TagFormat(string, tag="i")


def link(href: str, string: str | None = None) -> TagFormat:
    return TagFormat(
        string or href,
        tag="a",
        href=QUOT_MARK + href + QUOT_MARK,
    )


def pre_code(string: str, lang: str | ProgrammingLanguage | None = None) -> TagFormat:
    if lang is None:
        return TagFormat(string, tag="pre")
    lang = lang.value if isinstance(lang, ProgrammingLanguage) else lang
    return pre_code(TagFormat(string, tag="code", **{"class": f"language-{lang}"}))


def spoiler(string: str) -> TagFormat:
    return TagFormat(string, tag="tg-spoiler")


def start_bot_link(bot_id: str | int, data: str, string: str | None = None) -> TagFormat:
    return link(get_start_bot_link(bot_id, data), string)


def start_group_link(bot_id: str | int, data: str, string: str | None = None) -> TagFormat:
    return link(get_start_group_link(bot_id, data), string)


def strike(string: str) -> TagFormat:
    return TagFormat(string, tag="s")


def mention(string: str, user_id: int) -> TagFormat:
    return link(get_mention_link(user_id), string)


def tg_emoji(string: str, emoji_id: int) -> TagFormat:
    return TagFormat(string, tag="tg-emoji", **{"emoji-id": emoji_id})


def invite_chat_link(invite_link: str, string: str | None = None) -> TagFormat:
    return link(
        get_invite_chat_link(invite_link),
        string or f"https://t.me/joinchat/{invite_link}",
    )


def resolve_domain(username: str, string: str | None = None) -> TagFormat:
    return link(
        get_resolve_domain_link(username),
        string or f"t.me/{username}",
    )


def underline(string: str) -> TagFormat:
    return TagFormat(string, tag="u")


__all__ = (
    "FormatString",
    "HTMLFormatter",
    "SpecialFormat",
    "block_quote",
    "bold",
    "channel_boost_link",
    "code_inline",
    "escape",
    "get_channel_boost_link",
    "get_invite_chat_link",
    "get_mention_link",
    "get_resolve_domain_link",
    "get_start_bot_link",
    "get_start_group_link",
    "invite_chat_link",
    "italic",
    "link",
    "mention",
    "pre_code",
    "resolve_domain",
    "spoiler",
    "start_bot_link",
    "start_group_link",
    "strike",
    "tg_emoji",
    "underline",
)
