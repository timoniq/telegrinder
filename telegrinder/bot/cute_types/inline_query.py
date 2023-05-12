from telegrinder.types import InlineQuery, User
from telegrinder.api import API, APIError
from telegrinder.result import Result


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
        results: list | None = None,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        switch_pm_text: str | None = None,
        switch_pm_parameter: str | None = None,
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
