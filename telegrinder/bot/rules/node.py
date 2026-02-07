import typing

from kungfu.library.monad.result import Ok
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.scope import Scope

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.compose import run_agent
from telegrinder.node.utils import as_node

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

type Node = typing.Any


class NodeRule(ABCRule):
    nodes: tuple[tuple[str | None, Node], ...]

    def __init__(
        self,
        *nodes: Node | tuple[str, Node],
        agent: type[Agent] | None = None,
        roots: dict[type[typing.Any], typing.Any] | None = None,
    ) -> None:
        self.agent = (agent or EventLoopAgent).build(nodes=set(map(as_node, nodes)))
        self.nodes = tuple((x if isinstance(x, tuple) else (None, x)) for x in nodes)
        self.roots = roots

    async def check(self, per_event_scope: Scope, context: Context) -> bool:
        async with run_agent(
            self.agent,
            context,
            per_event_scope=per_event_scope,
            roots=self.roots,
        ) as result:
            match result:
                case Ok(scope):
                    for key, node in self.nodes:
                        if key is not None and node in scope:
                            context[key] = scope[node].value

                    return True
                case _:
                    return False


__all__ = ("NodeRule",)
