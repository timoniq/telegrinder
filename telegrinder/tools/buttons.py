from typing import Optional


class Button:
    def __init__(
        self,
        text: str,
        request_contact: Optional[bool] = False,
        request_location: Optional[bool] = False,
        request_poll: Optional[dict] = None,
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll

    def get_data(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class InlineButton:
    def __init__(
        self,
        text: str,
        url: str = None,
        login_url: dict = None,
        pay: bool = None,
        callback_data: str = None,
        callback_game: dict = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
    ):
        self.text = text
        self.url = url
        self.login_url = login_url
        self.pay = pay
        self.callback_data = callback_data
        self.callback_game = callback_game
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat

    def get_data(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}
