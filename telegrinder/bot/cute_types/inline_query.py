import typing

from telegrinder.api import ABCAPI, APIError
from telegrinder.result import Result
from telegrinder.types import InlineQuery, InlineQueryResult, User

from .base import BaseCute


class InlineQueryCute(BaseCute, InlineQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        results: list[InlineQueryResult | dict] | None = None,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        switch_pm_text: str | None = None,
        switch_pm_parameter: str | None = None,
    ) -> Result[bool, APIError]:
        return await self.ctx_api.answer_inline_query(
            self.id,
            results=results,  # type: ignore
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )  # NOTE: param results: implement dataclass instead of dict
