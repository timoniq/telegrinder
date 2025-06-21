from __future__ import annotations

import dataclasses
import typing

from telegrinder.node.scope import NodeScope, get_scope

if typing.TYPE_CHECKING:
    from telegrinder.node.base import IsNode


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node: IsNode | None
    value: typing.Any
    subnodes: dict[str, typing.Self]
    generator: typing.AsyncGenerator[typing.Any, typing.Any | None] | None = None

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.value!r}" + (" (ACTIVE)>" if self.generator else ">")

    async def close(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        if self.node is not None and get_scope(self.node) not in scopes:
            return

        for subnode in self.subnodes.values():
            await subnode.close(scopes=scopes)

        if self.generator is None:
            return
        try:
            await self.generator.asend(with_value)
        except StopAsyncIteration:
            self.generator = None


__all__ = ("NodeSession",)
