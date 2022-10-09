from telegrinder.types import InlineQuery, User
from telegrinder.api import API, APIError
from telegrinder.result import Result
import typing


class InlineQueryCute(InlineQuery):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def ctx_api(self) -> API:
        return self.api

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
