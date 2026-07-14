import typing

from kungfu.library.monad.result import Result

from telegrinder.api.error import APIError
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.objects import BotAccessSettings, ManagedBotUpdated, User


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

    @shortcut("set_managed_bot_access_settings", custom_params={"user_id"})
    async def set_access_settings(
        self,
        *,
        is_access_restricted: bool,
        added_user_ids: list[int] | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.set_managed_bot_access_settings()`, see the [documentation](https://core.telegram.org/bots/api#setmanagedbotaccesssettings)

        Use this method to change the access settings of a managed bot. Returns True
        on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose access settings will be changed.
        :param is_access_restricted: Pass True if only selected users can access the bot. The bot's owner can alwaysaccess it.

        :param added_user_ids: A JSON-serialized list of up to 10 identifiers of users who will have accessto the bot in addition to its owner. Ignored if is_access_restricted isFalse."""
        return await self.bound_api.set_managed_bot_access_settings(
            user_id=self.user.id if user_id is None else user_id,
            is_access_restricted=is_access_restricted,
            added_user_ids=added_user_ids,
            **other,
        )

    @shortcut("get_managed_bot_access_settings", custom_params={"user_id"})
    async def get_access_settings(
        self,
        *,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[BotAccessSettings, APIError]:
        """Shortcut `API.get_managed_bot_access_settings()`, see the [documentation](https://core.telegram.org/bots/api#getmanagedbotaccesssettings)

        Use this method to get the access settings of a managed bot. Returns a BotAccessSettings
        object on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose access settings will be returned."""
        return await self.bound_api.get_managed_bot_access_settings(
            user_id=self.user.id if user_id is None else user_id,
            **other,
        )


__all__ = ("ManagedBotUpdatedCute",)
