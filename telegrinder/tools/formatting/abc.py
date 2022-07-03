from abc import ABC, abstractmethod
from telegrinder.tools.parse_mode import get_mention_link
import typing

T = typing.TypeVar("T")


class ABCFormatter(ABC, str):
    PARSE_MODE: str

    @abstractmethod
    def escape(self: T) -> T:
        ...

    @abstractmethod
    def bold(self: T) -> T:
        ...

    @abstractmethod
    def italic(self: T) -> T:
        ...

    @abstractmethod
    def underline(self: T) -> T:
        ...

    @abstractmethod
    def strike(self: T) -> T:
        ...

    @abstractmethod
    def link(self: T, href: str) -> T:
        ...

    def mention(self: T, user_id: int) -> T:
        return self.link(get_mention_link(user_id))

    @abstractmethod
    def code_block(self: T) -> T:
        ...

    @abstractmethod
    def code_block_with_lang(self: T, lang: str) -> T:
        ...

    @abstractmethod
    def code_inline(self: T) -> T:
        ...
