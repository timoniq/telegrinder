import dataclasses
from typing import ClassVar, Dict, Protocol

import msgspec


class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]


@dataclasses.dataclass
class BaseButton:
    def get_data(self) -> dict:
        return {
            k: v
            if k != "callback_data" or isinstance(v, str)
            else msgspec.json.encode(v).decode()
            for k, v in dataclasses.asdict(self).items()
            if v is not None
        }


@dataclasses.dataclass
class Button(BaseButton):
    text: str
    request_contact: bool = False
    request_location: bool = False
    request_poll: dict | None = None
    web_app: dict | None = None


@dataclasses.dataclass
class InlineButton(BaseButton):
    text: str
    url: str | None = None
    login_url: dict | None = None
    pay: bool | None = None
    callback_data: dict | str | IsDataclass | msgspec.Struct | None = None
    callback_game: dict | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    web_app: dict | None = None
