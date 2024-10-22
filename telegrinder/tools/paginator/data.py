import dataclasses
import typing

type PageAction = OpenId | SwitchPage


@dataclasses.dataclass(slots=True, frozen=True)
class Page[T]:
    max_page: int
    page_number: int
    items: list[T]


@dataclasses.dataclass
class Filter:
    name: str
    value: str | bool = True


@dataclasses.dataclass(slots=True, frozen=True)
class OpenId:
    pg_key: str
    open_id: int
    filters: dict[str, typing.Any]


@dataclasses.dataclass(slots=True, frozen=True)
class SwitchPage:
    pg_key: str
    page_number: int
    filters: dict[str, typing.Any]


@typing.runtime_checkable
class PaginatedData(typing.Protocol):
    id: typing.Any


__all__ = ("OpenId", "Page", "PageAction", "PaginatedData", "SwitchPage")
