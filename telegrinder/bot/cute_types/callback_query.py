from telegrinder.types import CallbackQuery, User
from telegrinder.types.methods import APIMethods
from telegrinder.model import get_params
from telegrinder.api import API, APIError, Token
from telegrinder.result import Result
import typing


class CallbackQueryCute(CallbackQuery):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def ctx_api(self) -> API:
        return self.api

    async def answer(
        self,
        text: typing.Optional[str] = None,
        show_alert: typing.Optional[bool] = None,
        url: typing.Optional[str] = None,
        cache_time: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)
