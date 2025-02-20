import typing

from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.api.error import APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params
from telegrinder.model import get_params
from telegrinder.tools.magic import shortcut
from telegrinder.types.objects import PreCheckoutQuery, User


class PreCheckoutQueryCute(BaseCute[PreCheckoutQuery], PreCheckoutQuery, kw_only=True):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @shortcut("answer_pre_checkout_query", custom_params={"pre_checkout_query_id"})
    async def answer(
        self,
        ok: bool,
        *,
        error_message: str | None = None,
        pre_checkout_query_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_pre_checkout_query()`, see the [documentation](https://core.telegram.org/bots/api#answerprecheckoutquery)

        Once the user has confirmed their payment and shipping details, the Bot
        API sends the final confirmation in the form of an Update with the field pre_checkout_query.
        Use this method to respond to such pre-checkout queries. On success, True
        is returned. Note: The Bot API must receive an answer within 10 seconds after
        the pre-checkout query was sent."""
        params = compose_method_params(
            get_params(locals()), self, default_params={("pre_checkout_query_id", "id")}
        )
        return await self.ctx_api.answer_pre_checkout_query(**params)


__all__ = ("PreCheckoutQueryCute",)
