import typing

from kungfu.library.monad.result import Result

from telegrinder.api.api import APIError
from telegrinder.bot.cute_types.base import BaseCute, shortcut
from telegrinder.bot.cute_types.chat_member_updated import ChatMemberShortcuts, chat_member_interaction
from telegrinder.bot.cute_types.message import execute_method_answer
from telegrinder.types.objects import *

JOIN_REQUEST_QUERY: typing.Final = execute_method_answer(
    default_params={("chat_join_request_query_id", "query_id")},
)


class ChatJoinRequestCute(BaseCute[ChatJoinRequest], ChatJoinRequest, ChatMemberShortcuts, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def user_id(self) -> int:
        return self.from_user.id

    @shortcut(
        "answer_chat_join_request_query",
        executor=JOIN_REQUEST_QUERY,
        return_type=bool,
        custom_params={"chat_join_request_query_id"},
    )
    async def answer_query(
        self,
        result: typing.Literal["approve", "decline", "queue"],
        *,
        chat_join_request_query_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_chat_join_request_query()`, see the [documentation](https://core.telegram.org/bots/api#answerchatjoinrequestquery)

        Use this method to process a received chat join request query. Returns True
        on success.
        :param chat_join_request_query_id: [`CUSTOM PARAMETER`] Unique identifier of the join request query.

        :param result: Result of the query. Must be either `approve` to allow the user to join thechat, `decline` to disallow the user to join the chat, or `queue` to leavethe decision to other administrators."""
        ...

    @shortcut(
        "send_chat_join_request_web_app",
        executor=JOIN_REQUEST_QUERY,
        return_type=bool,
        custom_params={"chat_join_request_query_id"},
    )
    async def send_web_app(
        self,
        web_app_url: str,
        *,
        chat_join_request_query_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.send_chat_join_request_web_app()`, see the [documentation](https://core.telegram.org/bots/api#sendchatjoinrequestwebapp)

        Use this method to process a received chat join request query by showing
        a Mini App to the user before deciding the outcome. Call answerChatJoinRequestQuery
        to resolve the join request query based on the user interaction with the
        Mini App. Returns True on success.
        :param chat_join_request_query_id: [`CUSTOM PARAMETER`] Unique identifier of the join request query.

        :param web_app_url: An HTTPS URL of a Web App to be opened with additional data as specified inInitializing Web Apps."""
        ...

    @shortcut(
        "approve_chat_join_request",
        executor=chat_member_interaction,
        return_type=bool,
        custom_params={"chat_id", "user_id"},
    )
    async def approve(
        self,
        *,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.approve_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#approvechatjoinrequest)

        Use this method to approve a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success.
        :param chat_id: [`CUSTOM PARAMETER`] Unique identifier for the target chat or username of the target channelin the format @username.

        :param user_id: Unique identifier of the target user."""
        ...

    @shortcut(
        "decline_chat_join_request",
        executor=chat_member_interaction,
        return_type=bool,
        custom_params={"chat_id", "user_id"},
    )
    async def decline(
        self,
        *,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.decline_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#declinechatjoinrequest)

        Use this method to decline a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success.
        :param chat_id: [`CUSTOM PARAMETER`] Unique identifier for the target chat or username of the target channelin the format @username.

        :param user_id: Unique identifier of the target user."""
        ...


__all__ = ("ChatJoinRequestCute",)
