import typing

from fntypes.library.monad.result import Result

from telegrinder.api.api import APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params, shortcut
from telegrinder.types.methods_utils import get_params
from telegrinder.types.objects import *


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    @shortcut("answer_inline_query", custom_params={"results", "inline_query_id"})
    async def answer(
        self,
        results: InlineQueryResult | list[InlineQueryResult],
        *,
        button: InlineQueryResultsButton | None = None,
        cache_time: int | None = None,
        inline_query_id: str | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_inline_query()`, see the [documentation](https://core.telegram.org/bots/api#answerinlinequery)

        Use this method to send answers to an inline query. On success, True is returned.
        No more than 50 results per query are allowed."""
        params = compose_method_params(
            get_params(locals()),
            self,
            default_params={("inline_query_id", "id")},
        )
        params["results"] = [results] if not isinstance(results, list) else results
        return await self.ctx_api.answer_inline_query(**params)


__all__ = ("InlineQueryCute",)
