import enum
import html
import types
import typing
from string.templatelib import Template

from telegrinder.tools.formatting.deep_links.links import tg_mention_link
from telegrinder.tools.parse_mode import ParseMode

type FormatString = object | Template
type Formatter = typing.Callable[[FormatString], TagFormat]

TAG_FORMAT: typing.Final = "<{tag}{data}>{content}</{tag}>"
UNION_SPECIFIERS_SEPARATOR: typing.Final = "+"


def blockquote(s: FormatString, /, *, expandable: bool = False) -> TagFormat:
    return TagFormat(s, tag=Tag.BLOCK_QUOTE, **dict(expandable=None) if expandable is True else dict())


def bold(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.BOLD)


def code_inline(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.CODE)


def expandable_blockquote(s: FormatString, /) -> TagFormat:
    return blockquote(s, expandable=True)


monospace = code_inline


def italic(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.ITALIC)


def link(href: FormatString, /, *, text: str | None = None) -> TagFormat:
    return TagFormat(
        text or href,
        tag=Tag.HYPERLINK,
        href=f'"{href}"',
    )


def pre_code(s: FormatString, /, *, lang: str | None = None) -> TagFormat:
    if not lang:
        return TagFormat(s, tag=Tag.PRE)
    return pre_code(TagFormat(s, tag=Tag.CODE, **{"class": f"language-{lang}"}))


def spoiler(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.SPOILER)


def strike(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.STRIKE)


def mention(s: FormatString, /, *, user_id: int) -> TagFormat:
    text = escape(s) if isinstance(s, Template) else str(s)
    return link(tg_mention_link(user_id=user_id), text=text)


def tg_emoji(s: FormatString, /, *, emoji_id: int) -> TagFormat:
    return TagFormat(s, tag=Tag.EMOJI, emoji_id=f'"{emoji_id}"')


def underline(s: FormatString, /) -> TagFormat:
    return TagFormat(s, tag=Tag.UNDERLINE)


def _apply_formats(value: typing.Any, format_spec: str | None = None) -> str:
    if not format_spec:
        return html.escape(str(value))

    result: FormatString = html.escape(str(value))

    for fmt in (f.strip() for f in format_spec.split(UNION_SPECIFIERS_SEPARATOR)):
        if fmt in FORMATTERS:
            result = FORMATTERS[fmt](result)
        else:
            raise ValueError(f"Unknown format: `{fmt}`")

    return result.formatting() if isinstance(result, TagFormat) else result


def escape(s: FormatString, /) -> str:
    if isinstance(s, Template):
        parts: list[str] = []

        for item in s:
            if isinstance(item, str):
                parts.append(html.escape(item))
            else:
                value = item.value

                if isinstance(value, TagFormat):
                    parts.append(value.formatting())
                elif item.format_spec:
                    parts.append(_apply_formats(value, item.format_spec))
                else:
                    parts.append(html.escape(str(value)))

        return "".join(parts)

    return html.escape(str(s))


class HTMLMeta(type):
    def __lshift__[T](cls: typing.Callable[..., T], other: object, /) -> T:
        if not isinstance(other, str | Template | TagFormat):
            return NotImplemented
        return cls(other)


class Tag(enum.StrEnum):
    HYPERLINK = "a"
    BOLD = "b"
    ITALIC = "i"
    UNDERLINE = "u"
    STRIKE = "s"
    CODE = "code"
    PRE = "pre"
    SPOILER = "tg-spoiler"
    BLOCK_QUOTE = "blockquote"
    EMOJI = "tg-emoji"

    def __str__(self) -> str:
        return self.value


class TagFormat(str):
    __slots__ = ("data", "tag")

    tag: Tag
    data: dict[str, typing.Any]

    def __new__(cls, s: FormatString, /, *, tag: Tag, **data: typing.Any) -> typing.Self:
        s = escape(s) if not isinstance(s, TagFormat) else s.formatting()
        obj = super().__new__(cls, s)
        obj.data = data
        obj.tag = tag
        return obj

    def __str__(self) -> str:
        return self.formatting()

    @property
    def content(self) -> str:
        return super().__str__()

    @property
    def tag_data(self) -> str:
        return "".join(f" {k}={v}" if v is not None else f" {k}" for k, v in self.data.items())

    def formatting(self) -> str:
        return TAG_FORMAT.format(
            tag=self.tag,
            data=self.tag_data,
            content=self.content,
        )


class HTML(str, metaclass=HTMLMeta):
    """A class for creating and formatting HTML strings.

    >>> HTML << "Hello, " << bold("World!")
    'Hello, <b>World!</b>'

    >>> HTML << t"Hello, {name:underline}! " << "You are <b>{age}</b> years old."
    'Hello, <u>Arseny</u>! You are <b>20</b> years old.'
    """

    PARSE_MODE: typing.Final = ParseMode.HTML

    __slots__ = ()

    def __new__(cls, s: str | Template | TagFormat, /) -> typing.Self:
        if isinstance(s, Template):
            content = escape(s)
        elif isinstance(s, TagFormat):
            content = s.formatting()
        else:
            content = s

        return super().__new__(cls, content)

    def __lshift__(self, other: object, /) -> typing.Self:
        if isinstance(other, TagFormat):
            addition = other.formatting()
        elif isinstance(other, Template):
            addition = escape(other)
        else:
            addition = str(other)

        return self.__class__.__new__(self.__class__, self + addition)


FORMATTERS: types.MappingProxyType[str, Formatter] = types.MappingProxyType(
    mapping=dict(
        bold=bold,
        b=bold,
        code=code_inline,
        c=code_inline,
        monospace=monospace,
        italic=italic,
        i=italic,
        spoiler=spoiler,
        sp=spoiler,
        strike=strike,
        s=strike,
        underline=underline,
        u=underline,
        blockquote=blockquote,
        expandable_blockquote=expandable_blockquote,
    ),
)


__all__ = (
    "HTML",
    "Tag",
    "TagFormat",
    "blockquote",
    "bold",
    "code_inline",
    "escape",
    "expandable_blockquote",
    "italic",
    "link",
    "mention",
    "monospace",
    "pre_code",
    "spoiler",
    "strike",
    "tg_emoji",
    "underline",
)
