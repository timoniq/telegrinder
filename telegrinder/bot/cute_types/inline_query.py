import typing

from telegrinder.api import ABCAPI, APIError
from telegrinder.option import Nothing
from telegrinder.option.msgspec_option import Option
from telegrinder.result import Result
from telegrinder.types import InlineQuery, InlineQueryResult, User

from .base import BaseCute


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        results: list[InlineQueryResult | dict]
        | Option[list[InlineQueryResult | dict]],
        cache_time: int | Option[int] = Nothing,
        is_personal: bool | Option[bool] = Nothing,
        next_offset: str | Option[str] = Nothing,
        switch_pm_text: str | Option[str] = Nothing,
        switch_pm_parameter: str | Option[str] = Nothing,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        return await self.ctx_api.answer_inline_query(
            self.id,
            results=results,  # type: ignore
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
            **other,
        )  # NOTE: param results: implement dataclass instead of dict


__all__ = ("InlineQueryCute",)
