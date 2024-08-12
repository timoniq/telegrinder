import abc
import inspect
import typing

from telegrinder.api import ABCAPI, API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import get_annotations, magic_bundle

ComposeResult: typing.TypeAlias = (
    typing.Coroutine[typing.Any, typing.Any, typing.Any]
    | typing.AsyncGenerator[typing.Any, None]
    | typing.Any
)

NODE_IMPL_KEY = "_node_impl"

if typing.TYPE_CHECKING:
    node_impl = classmethod

else:

    def node_impl(func):
        setattr(func, NODE_IMPL_KEY, True)
        return func


def is_node(maybe_node: type[typing.Any]) -> typing.TypeGuard[type["Node"]]:
    maybe_node = typing.get_origin(maybe_node) or maybe_node
    return (
        isinstance(maybe_node, type)
        and issubclass(maybe_node, Node)
        or isinstance(maybe_node, Node)
        or hasattr(maybe_node, "as_node")
    )


def collect_context_annotations(function: typing.Callable[..., typing.Any]) -> dict[str, typing.Any]:
    return {k: v for k, v in get_annotations(function).items() if not is_node(v)}


def collect_nodes(function: typing.Callable[..., typing.Any]) -> dict[str, type["Node"]]:
    return {k: v for k, v in get_annotations(function).items() if is_node(v)}


def collect_node_impls(node_namespace: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {k: v for k, v in node_namespace.items() if getattr(v, NODE_IMPL_KEY, False) is True}


def get_node_impl(
    node: type[typing.Any],
    node_impls: dict[str, typing.Callable[..., typing.Any]],
) -> typing.Callable[..., typing.Any] | None:
    for n_impl in node_impls.values():
        if "return" in n_impl.__annotations__ and issubclass(node, n_impl.__annotations__["return"]):
            return n_impl
    return None


class ComposeError(BaseException):
    pass


class Node(abc.ABC):
    node: str = "node"
    scope: NodeScope = NodeScope.PER_EVENT

    __nodes__: dict[str, type["Node"]]
    __context_annotations__: dict[str, typing.Any]
    __node_impls__: dict[str, typing.Callable[..., typing.Any]]

    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ != "BaseNode":
            return
        cls.__node_impls__ = collect_node_impls(dict(vars(cls)))

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @classmethod
    async def compose_context_annotation(
        cls,
        annotation: typing.Any,
        update: UpdateCute,
        ctx: Context,
    ) -> typing.Any:
        orig_annotation: type[typing.Any] = typing.get_origin(annotation) or annotation
        n_impl = get_node_impl(orig_annotation, cls.get_node_impls())
        if n_impl is None:
            raise ComposeError(f"Node implementation for {orig_annotation.__name__!r} not found.")

        result = n_impl(
            cls, **magic_bundle(n_impl, {"update": update, "context": ctx}, start_idx=0, bundle_ctx=False)
        )
        if inspect.isawaitable(result):
            return await result
        return result

    @classmethod
    def compose_error(cls, error: str | None = None) -> typing.NoReturn:
        raise ComposeError(error)

    @classmethod
    def get_sub_nodes(cls) -> dict[str, type["Node"]]:
        if not hasattr(cls, "__nodes__"):
            cls.__nodes__ = collect_nodes(cls.compose)
        return cls.__nodes__

    @classmethod
    def get_context_annotations(cls) -> dict[str, typing.Any]:
        if not hasattr(cls, "__context_annotations__"):
            cls.__context_annotations__ = collect_context_annotations(cls.compose)
        return cls.__context_annotations__

    @classmethod
    def get_node_impls(cls) -> dict[str, typing.Callable[..., typing.Any]]:
        return cls.__node_impls__

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> bool:
        return inspect.isasyncgenfunction(cls.compose)


class BaseNode(Node, abc.ABC):
    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @node_impl
    async def compose_api(cls, update: UpdateCute) -> API:
        return update.ctx_api

    @node_impl
    async def compose_bound_api(cls, update: UpdateCute) -> ABCAPI:
        return update.api

    @node_impl
    async def compose_context(cls, context: Context) -> Context:
        return context

    @node_impl
    async def compose_update(cls, update: UpdateCute) -> UpdateCute:
        return update


class DataNode(BaseNode, abc.ABC):
    node = "data"

    @typing.dataclass_transform()
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> ComposeResult:
        pass


class ScalarNodeProto(BaseNode, abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> ComposeResult:
        pass


SCALAR_NODE = type("ScalarNode", (), {"node": "scalar"})


if typing.TYPE_CHECKING:

    class ScalarNode(ScalarNodeProto, abc.ABC):
        pass

else:

    def create_node(cls, bases, dct):
        dct.update(cls.__dict__)
        return type(cls.__name__, bases, dct)

    def create_class(name, bases, dct):
        return type(
            "Scalar",
            (SCALAR_NODE,),
            {
                "as_node": classmethod(lambda cls: create_node(cls, bases, dct)),
                "scope": Node.scope,
                **collect_node_impls(dict(vars(BaseNode))),
            },
        )

    class ScalarNode(ScalarNodeProto, abc.ABC, metaclass=create_class):
        pass


__all__ = (
    "ComposeError",
    "DataNode",
    "Node",
    "BaseNode",
    "SCALAR_NODE",
    "ScalarNode",
    "collect_nodes",
    "collect_context_annotations",
    "is_node",
    "node_impl",
)
