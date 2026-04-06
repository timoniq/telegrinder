import dataclasses
import enum
import typing

from telegrinder.bot.cute_types.chat_member_updated import ChatMemberUpdatedCute
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.objects import (
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
)

type _MemberStatus = MemberStatusFlag | MemberStatusUpdating
type ChatMember = typing.Union[
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
]


@dataclasses.dataclass(frozen=True, slots=True)
class MemberStatusUpdating:
    old: MemberStatusFlag
    new: MemberStatusFlag

    def __invert__(self) -> typing.Self:
        return dataclasses.replace(self, old=self.new, new=self.old)


class MemberStatusFlag(enum.IntFlag):
    CREATOR = enum.auto()
    ADMINISTRATOR = enum.auto()
    MEMBER = enum.auto()
    LEFT = enum.auto()
    KICKED = enum.auto()
    RESTRICTED = enum.auto()
    RESTRICTED_NOT_MEMBER = enum.auto()

    RESTRICTED_MEMBER = MEMBER | RESTRICTED

    IS_MEMBER = CREATOR | ADMINISTRATOR | MEMBER | RESTRICTED
    IS_NOT_MEMBER = LEFT | KICKED | RESTRICTED_NOT_MEMBER

    IS_ADMIN = CREATOR | ADMINISTRATOR
    IS_NOT_ADMIN = RESTRICTED_MEMBER | IS_NOT_MEMBER

    def __rshift__(self, other: object, /) -> MemberStatusUpdating:
        if not isinstance(other, type(self)):
            return NotImplemented
        return MemberStatusUpdating(old=self, new=other)

    def __lshift__(self, other: object, /) -> MemberStatusUpdating:
        if not isinstance(other, type(self)):
            return NotImplemented
        return MemberStatusUpdating(old=other, new=self)


class MemberStatus:
    CREATOR = MemberStatusFlag.CREATOR
    ADMINISTRATOR = MemberStatusFlag.ADMINISTRATOR
    MEMBER = MemberStatusFlag.MEMBER
    LEFT = MemberStatusFlag.LEFT
    KICKED = MemberStatusFlag.KICKED
    RESTRICTED = MemberStatusFlag.RESTRICTED_MEMBER | MemberStatusFlag.RESTRICTED_NOT_MEMBER

    RESTRICTED_MEMBER = MemberStatusFlag.RESTRICTED_MEMBER
    RESTRICTED_NOT_MEMBER = MemberStatusFlag.RESTRICTED_NOT_MEMBER

    IS_MEMBER = MemberStatusFlag.IS_MEMBER
    IS_NOT_MEMBER = ~IS_MEMBER

    IS_ADMIN = MemberStatusFlag.IS_ADMIN
    IS_NOT_ADMIN = ~IS_ADMIN

    JOIN = IS_NOT_MEMBER >> IS_MEMBER
    LEAVE = ~JOIN
    PROMOTED = (RESTRICTED_MEMBER | IS_NOT_MEMBER) >> ADMINISTRATOR


class ChatMemberUpdatedRule(ABCRule):
    def __init__(self, status: _MemberStatus, /) -> None:
        self.status = status

    def check_status(
        self,
        member: ChatMember,
        status: MemberStatusFlag,
        checking_status: MemberStatusFlag,
    ) -> bool:
        if (
            MemberStatusFlag.RESTRICTED_MEMBER in checking_status
            or MemberStatusFlag.RESTRICTED_NOT_MEMBER in checking_status
        ) and status == MemberStatusFlag.RESTRICTED:
            return (
                True
                if MemberStatus.RESTRICTED in checking_status
                else (getattr(member, "is_member", None) is (MemberStatusFlag.RESTRICTED_MEMBER in checking_status))
            )

        return status == checking_status or status in checking_status

    def check(self, event: ChatMemberUpdatedCute) -> bool:
        checking_new_status, checking_old_status = (
            (
                self.status.new,
                self.status.old,
            )
            if isinstance(self.status, MemberStatusUpdating)
            else (self.status, None)
        )
        new_member, old_member = event.new_chat_member.v, event.old_chat_member.v
        new_member_status, old_member_status = (
            MEMBER_STATUS_MAP[new_member.status],
            MEMBER_STATUS_MAP[old_member.status],
        )
        return (
            all(
                (
                    self.check_status(old_member, old_member_status, checking_old_status),
                    self.check_status(new_member, new_member_status, checking_new_status),
                ),
            )
            if checking_old_status is not None
            else self.check_status(new_member, new_member_status, checking_new_status)
        )


MEMBER_STATUS_MAP: typing.Final = {
    "creator": MemberStatusFlag.CREATOR,
    "administrator": MemberStatusFlag.ADMINISTRATOR,
    "member": MemberStatusFlag.MEMBER,
    "left": MemberStatusFlag.LEFT,
    "kicked": MemberStatusFlag.KICKED,
    "restricted": MemberStatusFlag.RESTRICTED,
}


__all__ = ("ChatMemberUpdatedRule", "MemberStatus")
