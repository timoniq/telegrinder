import dataclasses
import typing

type PaginatorButton = OpenIdButton | SwitchPageButton


@dataclasses.dataclass(slots=True, frozen=True)
class Page[T]:
    max_page: int
    page_number: int
    items: list[T]


@dataclasses.dataclass(slots=True, frozen=True)
class OpenIdButton:
    paginator: str
    open_id: int


@dataclasses.dataclass(slots=True, frozen=True)
class SwitchPageButton:
    paginator: str
    page_number: int


@typing.runtime_checkable
class PaginatedDataProtocol(typing.Protocol):
    id: typing.Any

    @classmethod
    async def fetch(cls, id: typing.Any) -> typing.Self: ...


__all__ = ("OpenIdButton", "Page", "PaginatedDataProtocol", "SwitchPageButton")
