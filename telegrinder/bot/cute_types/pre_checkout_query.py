import typing

from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.api.error import APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params, shortcut
from telegrinder.model import get_params
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
        pre_checkout_query_id: str | None = None,
        error_message: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_pre_checkout_query()`, see the [documentation](https://core.telegram.org/bots/api#answerprecheckoutquery)

        Once the user has confirmed their payment and shipping details, the Bot
        API sends the final confirmation in the form of an Update with the field pre_checkout_query.
        Use this method to respond to such pre-checkout queries. On success, True
        is returned. Note: The Bot API must receive an answer within 10 seconds after
        the pre-checkout query was sent.

        :param pre_checkout_query_id: Unique identifier for the query to be answered.

        :param ok: Specify True if everything is alright (goods are available, etc.) and the
        bot is ready to proceed with the order. Use False if there are any problems.

        :param error_message: Required if ok is False. Error message in human readable form that explains
        the reason for failure to proceed with the checkout (e.g. `Sorry, somebody
        just bought the last of our amazing black T-shirts while you were busy filling
        out your payment details. Please choose a different color or garment!`).
        Telegram will display this message to the user.
        """

        params = compose_method_params(get_params(locals()), self, default_params={("pre_checkout_query_id", "id")})
        return await self.ctx_api.answer_pre_checkout_query(**params)


__all__ = ("PreCheckoutQueryCute",)
