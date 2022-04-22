from telegrinder.types import CallbackQuery
from telegrinder.types.methods import APIMethods
from telegrinder.api import API, APIError
from telegrinder.tools import Result
import typing


class CallbackQueryCute(CallbackQuery):
    unprep_ctx_api: typing.Optional[typing.Any] = None

    @property
    def ctx_api(self) -> API:
        return getattr(self, "unprep_ctx_api")  # type: ignore

    async def answer(
        self,
        text: typing.Optional[str] = None,
        show_alert: typing.Optional[bool] = None,
        url: typing.Optional[str] = None,
        cache_time: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        params = APIMethods.get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)
