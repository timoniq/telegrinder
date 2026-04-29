import typing

from kungfu.library.monad.result import Result

from telegrinder.api.error import APIError
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.objects import ManagedBotUpdated, User


class ManagedBotUpdatedCute(BaseCute[ManagedBotUpdated], ManagedBotUpdated, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.user

    @shortcut("get_managed_bot_token", custom_params={"user_id"})
    async def get_token(
        self,
        *,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[str, APIError]:
        """Shortcut `API.get_managed_bot_token()`, see the [documentation](https://core.telegram.org/bots/api#getmanagedbottoken)

        Use this method to get the token of a managed bot. Returns the token as String
        on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose token will be returned."""
        return await self.bound_api.get_managed_bot_token(
            user_id=self.user.id if user_id is None else user_id,
            **other,
        )


__all__ = ("ManagedBotUpdatedCute",)
