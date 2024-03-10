import typing

from fntypes.result import Result

from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.msgspec_utils import Nothing, Option
from telegrinder.types import (
    InlineQuery,
    InlineQueryResult,
    InlineQueryResultsButton,
    User,
)

from .base import BaseCute


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        results: InlineQueryResult | list[InlineQueryResult],
        inline_query_id: str | Option[str] = Nothing,
        cache_time: int | Option[int] = Nothing,
        is_personal: bool | Option[bool] = Nothing,
        next_offset: str | Option[str] = Nothing,
        button: Option[InlineQueryResultsButton] | InlineQueryResultsButton = Nothing,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        params["results"] = [results] if not isinstance(results, list) else results
        params.setdefault("inline_query_id", self.id)
        return await self.ctx_api.answer_inline_query(**params)


__all__ = ("InlineQueryCute",)
