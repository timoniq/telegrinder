from __future__ import annotations

import dataclasses
import typing

from telegrinder.modules import logger
from telegrinder.node.exceptions import ComposeError
from telegrinder.node.scope import NodeScope, get_scope
from telegrinder.tools.aio import Generator, stop_generator
from telegrinder.tools.fullname import fullname

if typing.TYPE_CHECKING:
    from telegrinder.node.base import IsNode


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node: IsNode
    value: typing.Any
    generator: Generator[typing.Any, typing.Any, typing.Any] | None = None

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.value!r}" + (" (ACTIVE)>" if self.generator else ">")

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


__all__ = ("NodeSession",)
