import dataclasses


class BaseButton:
    def get_data(self) -> dict:
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}  # type: ignore


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
    callback_data: str | None = None
    callback_game: dict | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    web_app: dict | None = None
