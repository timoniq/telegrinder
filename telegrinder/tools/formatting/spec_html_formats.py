import dataclasses
import typing

from telegrinder.types.enums import ProgrammingLanguage

SpecialFormat = typing.Union[
    "ChannelBoostLink",
    "Mention",
    "Link",
    "PreCode",
    "TgEmoji",
    "StartBotLink",
    "StartGroupLink",
    "ResolveDomain",
    "InviteChatLink",
]


def is_spec_format(obj: typing.Any) -> typing.TypeGuard[SpecialFormat]:
    return (
        dataclasses.is_dataclass(obj)
        and hasattr(obj, "__formatter_name__")
        and isinstance(obj, BaseSpecFormat)
    )


@dataclasses.dataclass(repr=False)
class BaseSpecFormat:
    __formatter_name__: typing.ClassVar[str]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__!r}: {self.__formatter_name__!r}>"


@dataclasses.dataclass
class ChannelBoostLink(BaseSpecFormat):
    __formatter_name__ = "channel_boost_link"

    channel_username: str
    string: str | None = None


@dataclasses.dataclass
class InviteChatLink(BaseSpecFormat):
    __formatter_name__ = "invite_chat_link"

    invite_link: str
    string: str | None = None


@dataclasses.dataclass
class Mention(BaseSpecFormat):
    __formatter_name__ = "mention"

    string: str
    user_id: int


@dataclasses.dataclass
class Link(BaseSpecFormat):
    __formatter_name__ = "link"

    href: str
    string: str | None = None


@dataclasses.dataclass
class PreCode(BaseSpecFormat):
    __formatter_name__ = "pre_code"

    string: str
    lang: str | ProgrammingLanguage | None = None


@dataclasses.dataclass
class TgEmoji(BaseSpecFormat):
    __formatter_name__ = "tg_emoji"
    
    string: str
    emoji_id: int


@dataclasses.dataclass
class StartBotLink(BaseSpecFormat):
    __formatter_name__ = "start_bot_link"

    bot_username: str
    data: str
    string: str | None


@dataclasses.dataclass
class StartGroupLink(BaseSpecFormat):
    __formatter_name__ = "start_group_link"

    bot_username: str
    data: str
    string: str | None = None


@dataclasses.dataclass
class ResolveDomain(BaseSpecFormat):
    __formatter_name__ = "resolve_domain"

    username: str
    string: str | None = None


__all__ = (
    "BaseSpecFormat",
    "ChannelBoostLink",
    "InviteChatLink",
    "Link",
    "Mention",
    "PreCode",
    "ResolveDomain",
    "SpecialFormat",
    "StartBotLink",
    "StartGroupLink",
    "TgEmoji",
)
