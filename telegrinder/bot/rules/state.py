import dataclasses
import enum
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.source import Source

if typing.TYPE_CHECKING:
    from telegrinder.tools.state_storage.abc import ABCStateStorage

Payload = typing.TypeVar("Payload")


class StateMeta(enum.Enum):
    NO_STATE = enum.auto()
    ANY = enum.auto()


@dataclasses.dataclass(frozen=True, slots=True)
class State(ABCRule, typing.Generic[Payload]):
    storage: "ABCStateStorage[Payload]"
    key: str | StateMeta | enum.Enum

    async def check(self, source: Source, ctx: Context) -> bool:
        state = await self.storage.get(source.from_user.id)
        if not state:
            return self.key == StateMeta.NO_STATE

        if self.key != StateMeta.ANY and self.key != state.unwrap().key:
            return False

        ctx["state"] = state.unwrap()
        return True


__all__ = ("State", "StateMeta")
