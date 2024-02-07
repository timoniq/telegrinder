import typing

from fntypes.result import Result

from telegrinder.api import ABCAPI, APIError
from telegrinder.msgspec_utils import Nothing, Option
from telegrinder.types import InlineQuery, InlineQueryResult, User

from .base import BaseCute


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        results: InlineQueryResult | list[InlineQueryResult],
        cache_time: int | Option[int] = Nothing,
        is_personal: bool | Option[bool] = Nothing,
        next_offset: str | Option[str] = Nothing,
        switch_pm_text: str | Option[str] = Nothing,
        switch_pm_parameter: str | Option[str] = Nothing,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        return await self.ctx_api.answer_inline_query(
            self.id,
            results=[results] if not isinstance(results, list) else results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
            **other,
        )


__all__ = ("InlineQueryCute",)
