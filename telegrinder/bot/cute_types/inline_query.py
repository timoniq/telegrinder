import typing

from fntypes.result import Result

from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.types import (
    InlineQuery,
    InlineQueryResult,
    InlineQueryResultsButton,
    User,
)

from .base import BaseCute, compose_method_params, shortcut


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    @shortcut("answer_inline_query", custom_params={"results"})
    async def answer(
        self,
        results: InlineQueryResult | list[InlineQueryResult],
        inline_query_id: str | None = None,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: InlineQueryResultsButton | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_inline_query()`, see the [documentation](https://core.telegram.org/bots/api#answerinlinequery)

        Use this method to send answers to an inline query. On success, True is returned. 
        No more than 50 results per query are allowed.

        :param inline_query_id: Unique identifier for the answered query.

        :param results: A JSON-serialized array of results for the inline query.

        :param cache_time: The maximum amount of time in seconds that the result of the inline query \
        may be cached on the server. Defaults to 300.

        :param is_personal: Pass True if results may be cached on the server side only for the user that \
        sent the query. By default, results may be returned to any user who sends \
        the same query.

        :param next_offset: Pass the offset that a client should send in the next query with the same text \
        to receive more results. Pass an empty string if there are no more results \
        or if you don't support pagination. Offset length can't exceed 64 bytes. \

        :param button: A JSON-serialized object describing a button to be shown above inline query \
        results.
        """

        params = compose_method_params(
            get_params(locals()),
            self,
            default_params={("inline_query_id", "id")},
        )
        params["results"] = [results] if not isinstance(results, list) else results
        return await self.ctx_api.answer_inline_query(**params)


__all__ = ("InlineQueryCute",)
