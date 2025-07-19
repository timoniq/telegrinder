from __future__ import annotations

import typing
from collections import deque
from reprlib import recursive_repr

from telegrinder.modules import logger
from telegrinder.node.exceptions import ComposeError
from telegrinder.node.scope import NodeScope, get_scope
from telegrinder.tools.aio import Generator, stop_generator
from telegrinder.tools.fullname import fullname

if typing.TYPE_CHECKING:
    from telegrinder.node.base import IsNode


async def close_sessions(
    sessions_map: dict[IsNode, NodeSession],
    /,
    *,
    scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    with_value: typing.Any | None = None,
    clear_sessions: bool = True,
    reverse: bool = True,
) -> None:
    input_sessions = sessions_map.values()
    stack = deque(input_sessions)
    output = deque[NodeSession]()

    while stack:
        session = stack.pop()
        if session.is_active and get_scope(session.node) in scopes:
            stack.extend(session.subsessions.values())
            if session not in output:
                output.appendleft(session) if not reverse and session in input_sessions else output.append(session)

    for session in output:
        await session.close(with_value, scopes=scopes)

    if clear_sessions and sessions_map:
        sessions_map.clear()


class NodeSession:
    subsessions: dict[IsNode, NodeSession]

    __slots__ = ("node", "value", "generator", "subsessions")

    def __init__(
        self,
        node: IsNode,
        value: typing.Any,
        generator: Generator[typing.Any, typing.Any, typing.Any] | None = None,
    ) -> None:
        self.node = node
        self.value = value
        self.generator = generator
        self.subsessions = {}

    @property
    def is_active(self) -> bool:
        return self.generator is not None

    @recursive_repr()
    def __repr__(self) -> str:
        return "<{}{}: node={!r}, value={!r}, subsessions={!r}>".format(
            type(self).__name__,
            (" (ACTIVE)" if self.is_active else ""),
            self.node,
            self.value,
            self.subsessions,
        )

    async def close(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> typing.Any | None:
        result = None

        if self.generator is not None and get_scope(self.node) in scopes:
            try:
                result = await stop_generator(self.generator, with_value)
            except ComposeError as compose_error:
                logger.debug(
                    "Caught compose error when closing session for node `{}`: {}",
                    fullname(self.node),
                    compose_error.message,
                )
            except BaseException as exception:
                logger.debug(
                    "Uncaught {!r} was occurred when closing session for node `{}`",
                    exception,
                    fullname(self.node),
                )
            finally:
                self.generator = None

        return result


__all__ = ("NodeSession", "close_sessions")
