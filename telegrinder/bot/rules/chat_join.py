import typing

from telegrinder.bot.cute_types import ChatJoinRequestCute
from telegrinder.bot.rules.abc import ABCRule

ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute


class HasInviteLink(ABCRule):
    def check(self, event: ChatJoinRequest) -> bool:
        return bool(event.invite_link)


class InviteLinkName(ABCRule, requires=[HasInviteLink()]):
    def __init__(self, name: str, /) -> None:
        self.name = name

    def check(self, event: ChatJoinRequest) -> bool:
        return event.invite_link.unwrap().name.unwrap_or_none() == self.name


class InviteLinkByCreator(ABCRule, requires=[HasInviteLink()]):
    def __init__(self, creator_id: int, /) -> None:
        self.creator_id = creator_id

    def check(self, event: ChatJoinRequest) -> bool:
        return event.invite_link.unwrap().creator.id == self.creator_id


__all__ = ("HasInviteLink", "InviteLinkByCreator", "InviteLinkName")
