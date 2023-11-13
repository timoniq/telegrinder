import dataclasses
import typing

import msgspec

from telegrinder.model import encoder


class DataclassInstance(typing.Protocol):
    __dataclass_fields__: typing.ClassVar[dict[str, dataclasses.Field[typing.Any]]]


@dataclasses.dataclass
class BaseButton:
    def get_data(self) -> dict[str, typing.Any]:
        return {
            k: v
            if k != "callback_data" or isinstance(v, str)
            else encoder.encode(v).decode()
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
    callback_data: typing.Union[
        str,
        dict[str, typing.Any],
        DataclassInstance,
        msgspec.Struct,
    ] | None = None
    callback_game: dict | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    web_app: dict | None = None
