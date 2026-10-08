import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.methods import APIResult
from telegrinder.types.objects import BotAccessSettings, ManagedBotUpdated, User
from telegrinder.types.utils import get_params


async def managed_bot_interaction(
    update: "ManagedBotUpdatedCute",
    method_name: str,
    params: dict[str, typing.Any],
    _result_type: typing.Any,
) -> APIResult[typing.Any]:
    params = get_params(params)
    params.setdefault("user_id", update.bot.id)
    return await getattr(update.bound_api, method_name)(**params)


class ManagedBotUpdatedCute(BaseCute[ManagedBotUpdated], ManagedBotUpdated, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.user

    @shortcut(
        "get_managed_bot_token",
        executor=managed_bot_interaction,
        return_type=APIResult[str],
        custom_params={"user_id"},
    )
    async def get_token(
        self,
        *,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> APIResult[str]:
        """Shortcut `API.get_managed_bot_token()`, see the [documentation](https://core.telegram.org/bots/api#getmanagedbottoken)

        Use this method to get the token of a managed bot. Returns the token as String
        on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose token will be returned."""
        ...

    @shortcut(
        "replace_managed_bot_token",
        executor=managed_bot_interaction,
        return_type=APIResult[str],
        custom_params={"user_id"},
    )
    async def replace_token(
        self,
        *,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> APIResult[str]:
        """Shortcut `API.replace_managed_bot_token()`, see the [documentation](https://core.telegram.org/bots/api#replacemanagedbottoken)

        Use this method to revoke the current token of a managed bot and generate
        a new one. Returns the new token as String on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose token will be replaced."""
        ...

    @shortcut(
        "set_managed_bot_access_settings",
        executor=managed_bot_interaction,
        return_type=APIResult[bool],
        custom_params={"user_id"},
    )
    async def set_access_settings(
        self,
        *,
        is_access_restricted: bool,
        added_user_ids: list[int] | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> APIResult[bool]:
        """Shortcut `API.set_managed_bot_access_settings()`, see the [documentation](https://core.telegram.org/bots/api#setmanagedbotaccesssettings)

        Use this method to change the access settings of a managed bot. Returns True
        on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose access settings will be changed.
        :param is_access_restricted: Pass True if only selected users can access the bot. The bot's owner can alwaysaccess it.

        :param added_user_ids: A JSON-serialized list of up to 10 identifiers of users who will have accessto the bot in addition to its owner. Ignored if is_access_restricted isFalse."""
        ...

    @shortcut(
        "get_managed_bot_access_settings",
        executor=managed_bot_interaction,
        return_type=APIResult[BotAccessSettings],
        custom_params={"user_id"},
    )
    async def get_access_settings(
        self,
        *,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> APIResult[BotAccessSettings]:
        """Shortcut `API.get_managed_bot_access_settings()`, see the [documentation](https://core.telegram.org/bots/api#getmanagedbotaccesssettings)

        Use this method to get the access settings of a managed bot. Returns a BotAccessSettings
        object on success.
        :param user_id: [`CUSTOM PARAMETER`] User identifier of the managed bot whose access settings will be returned."""
        ...


__all__ = ("ManagedBotUpdatedCute",)
