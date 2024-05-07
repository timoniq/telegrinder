import abc
import typing

from telegrinder.bot.cute_types import ChatJoinRequestCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter import EventAdapter

from .abc import ABCRule

ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute


class ChatJoinRequestRule(ABCRule[ChatJoinRequestCute], requires=[]):
    adapter = EventAdapter("chat_join_request", ChatJoinRequest)

    @abc.abstractmethod
    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        pass


class HasInviteLink(ChatJoinRequestRule):
    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return bool(event.invite_link)


class InviteLinkName(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, name: str, /) -> None:
        self.name = name

    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return event.invite_link.unwrap().name.unwrap_or_none() == self.name


class InviteLinkByCreator(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, creator_id: int, /) -> None:
        self.creator_id = creator_id

    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return event.invite_link.unwrap().creator.id == self.creator_id


__all__ = (
    "ChatJoinRequestRule",
    "HasInviteLink",
    "InviteLinkByCreator",
    "InviteLinkName",
)
