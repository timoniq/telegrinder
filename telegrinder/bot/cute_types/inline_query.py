from telegrinder.types import InlineQuery
from telegrinder.api import API, APIError
from telegrinder.tools import Result
import typing


class InlineQueryCute(InlineQuery):
    unprep_ctx_api: typing.Optional[typing.Any] = None

    @property
    def ctx_api(self) -> API:
        return getattr(self, "unprep_ctx_api")  # type: ignore

    async def answer(
        self,
        results: typing.Optional[list] = None,
        cache_time: typing.Optional[int] = None,
        is_personal: typing.Optional[bool] = None,
        next_offset: typing.Optional[str] = None,
        switch_pm_text: typing.Optional[str] = None,
        switch_pm_parameter: typing.Optional[str] = None,
    ) -> Result[bool, APIError]:
        return await self.ctx_api.answer_inline_query(
            self.id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )
