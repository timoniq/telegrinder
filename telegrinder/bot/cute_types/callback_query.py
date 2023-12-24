from telegrinder.api import API, APIError
from telegrinder.model import get_params
from telegrinder.result import Result
from telegrinder.types import CallbackQuery, User


class CallbackQueryCute(CallbackQuery, kw_only=True):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def ctx_api(self) -> API:
        return self.api

    async def answer(
        self,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
        **other
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)
