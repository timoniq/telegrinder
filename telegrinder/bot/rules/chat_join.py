import abc
import typing

from telegrinder.bot.cute_types import ChatJoinRequestCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.types.enums import UpdateType

from .abc import ABCRule, CheckResult

ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute


class ChatJoinRequestRule(ABCRule[ChatJoinRequest], requires=[]):
    adapter: EventAdapter[ChatJoinRequest] = EventAdapter(UpdateType.CHAT_JOIN_REQUEST, ChatJoinRequest)

    @abc.abstractmethod
    def check(self, event: ChatJoinRequest, context: Context) -> CheckResult:
        pass


class HasInviteLink(ChatJoinRequestRule):
    def check(self, event: ChatJoinRequest) -> bool:
        return bool(event.invite_link)


class InviteLinkName(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, name: str, /) -> None:
        self.name = name

    def check(self, event: ChatJoinRequest) -> bool:
        return event.invite_link.unwrap().name.unwrap_or_none() == self.name


class InviteLinkByCreator(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, creator_id: int, /) -> None:
        self.creator_id = creator_id

    def check(self, event: ChatJoinRequest) -> bool:
        return event.invite_link.unwrap().creator.id == self.creator_id


__all__ = (
    "ChatJoinRequestRule",
    "HasInviteLink",
    "InviteLinkByCreator",
    "InviteLinkName",
)
