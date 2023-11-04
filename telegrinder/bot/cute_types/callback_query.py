import typing

from telegrinder.api import ABCAPI, API, APIError
from telegrinder.model import get_params
from telegrinder.result import Result
from telegrinder.types import CallbackQuery, User


class CallbackQueryCute(CallbackQuery):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    @property
    def from_user(self) -> User:
        return self.from_

    @classmethod
    def from_update(cls, update: CallbackQuery, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)

    async def answer(
        self,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
        **other,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)

    def to_dict(self):
        return super().to_dict(exclude_fields={"api"})
