import typing
from contextlib import contextmanager

from kungfu.library.monad.result import Error, Ok
from nodnod.agent.base import Agent
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.interface.agent_from_node import create_agent_from_node

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.node.compose import compose

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.process import check_rule
    from telegrinder.bot.rules.abc import ABCRule

else:

    def check_rule(*args: typing.Any, **kwargs: typing.Any) -> bool:
        from telegrinder.bot.dispatch.process import check_rule

        return check_rule(*args, **kwargs)


type AnyNode = typing.Any
type Value = typing.Any


class FilterMiddleware(ABCMiddleware):
    source_filters: dict[AnyNode, tuple[type[Agent], dict[Value, tuple[ABCRule, ...]]]]
    _source_node_agents: dict[AnyNode, Agent]

    def __init__(self) -> None:
        self.source_filters = dict()
        self._source_node_agents = dict()

    async def pre(self, context: Context) -> bool:
        for source_node, (agent_cls, source_filter) in self.source_filters.items():
            if source_node not in self._source_node_agents:
                agent = self._source_node_agents[source_node] = create_agent_from_node(source_node, agent_cls=agent_cls)
            else:
                agent = self._source_node_agents[source_node]

            async with compose(source_node, context, agent=agent) as result:
                match result:
                    case Error(_):
                        return False
                    case Ok(value) if value not in source_filter:
                        return False
                    case _:
                        for filter in source_filter[result.value]:
                            if not await check_rule(filter, context):
                                return False

            return True

        return True

    @contextmanager
    def hold(
        self,
        source_node: AnyNode,
        source_value: Value,
        /,
        *filters: ABCRule,
        agent_cls: type[Agent] | None = None,
    ) -> typing.Generator[None, typing.Any, None]:
        try:
            self.source_filters.setdefault(source_node, (agent_cls or EventLoopAgent, {}))[1][source_value] = filters
            yield
        finally:
            self.release(source_node, source_value)

    def release(self, source_node: AnyNode, source_value: Value, /) -> None:
        source_filter = self.source_filters.get(source_node)

        if source_filter is not None:
            _, source_filter = source_filter
            source_filter.pop(source_value, None)

            if not source_filter:
                self.source_filters.pop(source_node, None)
                self._source_node_agents.pop(source_node, None)
        else:
            self._source_node_agents.pop(source_node, None)


__all__ = ("FilterMiddleware",)
