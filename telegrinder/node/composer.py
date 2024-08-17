import dataclasses
import typing

from fntypes.error import UnwrapError

from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import (
    BaseNode,
    ComposeError,
    Node,
    NodeScope,
    get_compose_annotations,
    get_nodes,
)
from telegrinder.tools.magic import magic_bundle

CONTEXT_STORE_NODES_KEY = "_node_ctx"


async def compose_node(
    _node: type[Node],
    update: UpdateCute,
    ctx: Context,
) -> "NodeSession":
    node = _node.as_node()
    context = NodeCollection({})
    node_ctx: dict[type[Node], "NodeSession"] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})

    for name, subnode in node.get_sub_nodes().items():
        if subnode in node_ctx:
            context.sessions[name] = node_ctx[subnode]
        else:
            context.sessions[name] = await compose_node(subnode, update, ctx)

            if getattr(subnode, "scope", None) is NodeScope.PER_EVENT:
                node_ctx[subnode] = context.sessions[name]

    for name, annotation in node.get_compose_annotations().items():
        context.sessions[name] = NodeSession(
            None,
            await node.compose_annotation(annotation, update, ctx),
            {},
        )

    if node.is_generator():
        generator = typing.cast(typing.AsyncGenerator[typing.Any, None], node.compose(**context.values()))
        value = await generator.asend(None)
    else:
        generator = None
        value = await typing.cast(typing.Awaitable[typing.Any], node.compose(**context.values()))

    return NodeSession(_node, value, context.sessions, generator)


async def compose_nodes(
    update: UpdateCute,
    ctx: Context,
    nodes: dict[str, type[Node]],
    node_class: type[Node] | None = None,
    compose_annotations: dict[str, typing.Any] | None = None,
) -> "NodeCollection | None":
    node_sessions: dict[str, NodeSession] = {}
    node_ctx: dict[type[Node], "NodeSession"] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})

    try:
        for name, node_t in nodes.items():
            scope = getattr(node_t, "scope", None)

            if scope is NodeScope.PER_EVENT and node_t in node_ctx:
                node_sessions[name] = node_ctx[node_t]
                continue
            elif scope is NodeScope.GLOBAL and hasattr(node_t, "_value"):
                node_sessions[name] = getattr(node_t, "_value")
                continue

            node_sessions[name] = await compose_node(node_t, update, ctx)

            if scope is NodeScope.PER_EVENT:
                node_ctx[node_t] = node_sessions[name]
            elif scope is NodeScope.GLOBAL:
                setattr(node_t, "_value", node_sessions[name])
    except (ComposeError, UnwrapError) as exc:
        logger.debug(f"Composing node (name={name!r}, node_class={node_t!r}) failed with error: {str(exc)!r}")
        await NodeCollection(node_sessions).close_all()
        return None

    if compose_annotations:
        node_class = node_class or BaseNode

        try:
            for name, annotation in compose_annotations.items():
                node_sessions[name] = await node_class.compose_annotation(annotation, update, ctx)
        except (ComposeError, UnwrapError) as exc:
            logger.debug(
                f"Composing context annotation (name={name!r}, annotation={annotation!r}) failed with error: {str(exc)!r}",
            )
            await NodeCollection(node_sessions).close_all()
            return None

    return NodeCollection(node_sessions)


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node_type: type[Node] | None
    value: typing.Any
    subnodes: dict[str, typing.Self]
    generator: typing.AsyncGenerator[typing.Any, typing.Any | None] | None = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.value!r}" + (" ACTIVE>" if self.generator else ">")

    async def close(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        if self.node_type and getattr(self.node_type, "scope", None) not in scopes:
            return

        for subnode in self.subnodes.values():
            await subnode.close(scopes=scopes)

        if self.generator is None:
            return
        try:
            await self.generator.asend(with_value)
        except StopAsyncIteration:
            self.generator = None


class NodeCollection:
    __slots__ = ("sessions",)

    def __init__(self, sessions: dict[str, NodeSession]) -> None:
        self.sessions = sessions

    def __repr__(self) -> str:
        return "<{}: sessions={!r}>".format(self.__class__.__name__, self.sessions)

    def values(self) -> dict[str, typing.Any]:
        return {name: session.value for name, session in self.sessions.items()}

    async def close_all(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        for session in self.sessions.values():
            await session.close(with_value, scopes=scopes)


@dataclasses.dataclass(slots=True, repr=False)
class Composition:
    func: typing.Callable[..., typing.Any]
    is_blocking: bool
    node_class: type[Node] = dataclasses.field(default_factory=lambda: BaseNode)
    nodes: dict[str, type[Node]] = dataclasses.field(init=False)
    compose_annotations: dict[str, typing.Any] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.nodes = get_nodes(self.func)
        self.compose_annotations = get_compose_annotations(self.func)

    def __repr__(self) -> str:
        return "<{}: for function={!r} with nodes={!r}, compose_annotations={!r}>".format(
            ("blocking " if self.is_blocking else "") + self.__class__.__name__,
            self.func.__qualname__,
            self.nodes,
            self.compose_annotations,
        )

    async def compose_nodes(self, update: UpdateCute, context: Context) -> NodeCollection | None:
        return await compose_nodes(
            update=update,
            ctx=context,
            nodes=self.nodes,
            node_class=self.node_class,
            compose_annotations=self.compose_annotations,
        )

    async def __call__(self, **kwargs: typing.Any) -> typing.Any:
        return await self.func(**magic_bundle(self.func, kwargs, start_idx=0, bundle_ctx=False))  # type: ignore


__all__ = ("Composition", "NodeCollection", "NodeSession", "compose_node", "compose_nodes")
