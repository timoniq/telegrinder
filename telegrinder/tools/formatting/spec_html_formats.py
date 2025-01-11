import dataclasses
import typing

from telegrinder.types.enums import ProgrammingLanguage

SpecialFormat: typing.TypeAlias = typing.Union[
    "BlockQuote",
    "Link",
    "Mention",
    "PreCode",
    "TgEmoji",
]


def is_spec_format(obj: typing.Any) -> typing.TypeGuard[SpecialFormat]:
    return dataclasses.is_dataclass(obj) and hasattr(obj, "__formatter_name__") and isinstance(obj, Base)


@dataclasses.dataclass(repr=False)
class Base:
    __formatter_name__: typing.ClassVar[str] = dataclasses.field(init=False, repr=False)

    def __repr__(self) -> str:
        return f"<Special formatter {self.__class__.__name__!r} -> {self.__formatter_name__!r}>"


@dataclasses.dataclass(repr=False, slots=True)
class Mention(Base):
    __formatter_name__ = "mention"

    string: str
    user_id: int


@dataclasses.dataclass(repr=False, slots=True)
class Link(Base):
    __formatter_name__ = "link"

    href: str
    string: str | None = None


@dataclasses.dataclass(repr=False, slots=True)
class PreCode(Base):
    __formatter_name__ = "pre_code"

    string: str
    lang: str | ProgrammingLanguage | None = None


@dataclasses.dataclass(repr=False, slots=True)
class TgEmoji(Base):
    __formatter_name__ = "tg_emoji"

    string: str
    emoji_id: int


@dataclasses.dataclass(repr=False, slots=True)
class BlockQuote(Base):
    __formatter_name__ = "block_quote"

    string: str
    expandable: bool = False


__all__ = (
    "Base",
    "BlockQuote",
    "Link",
    "Mention",
    "PreCode",
    "SpecialFormat",
    "TgEmoji",
)
