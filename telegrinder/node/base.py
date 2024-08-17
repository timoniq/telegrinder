import abc
import inspect
import typing
from types import AsyncGeneratorType

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import (
    NODE_IMPL_MARK,
    cache_magic_value,
    get_annotations,
    get_impls_by_key,
    magic_bundle,
    node_impl,
)

ComposeResult: typing.TypeAlias = typing.Awaitable[typing.Any] | typing.AsyncGenerator[typing.Any, None]


def is_node(maybe_node: type[typing.Any]) -> typing.TypeGuard[type["Node"]]:
    maybe_node = typing.get_origin(maybe_node) or maybe_node
    return (
        isinstance(maybe_node, type)
        and issubclass(maybe_node, Node)
        or isinstance(maybe_node, Node)
        or hasattr(maybe_node, "as_node")
    )


def get_impls_with_return_type(functions: typing.Iterable[typing.Callable[..., typing.Any]]) -> dict[typing.Any, typing.Callable[..., typing.Any]]:
    return {
        typing.get_origin(f.__annotations__["return"]) or f.__annotations__["return"]: f
        for f in functions
    }


@cache_magic_value("__compose_annotations__")
def get_compose_annotations(function: typing.Callable[..., typing.Any]) -> dict[str, typing.Any]:
    return {k: v for k, v in get_annotations(function).items() if not is_node(v)}


@cache_magic_value("__nodes__")
def get_nodes(function: typing.Callable[..., typing.Any]) -> dict[str, type["Node"]]:
    return {k: v for k, v in get_annotations(function).items() if is_node(v)}


@cache_magic_value("__is_generator__")
def is_generator(function: typing.Callable[..., typing.Any]) -> typing.TypeGuard[AsyncGeneratorType[typing.Any, None]]:
    return inspect.isasyncgenfunction(function)


def get_node_impls(node_cls: type["Node"]) -> dict[typing.Any, typing.Callable[..., typing.Any]]:
    if not hasattr(node_cls, "__node_impls__"):
        impls = get_impls_with_return_type(get_impls_by_key(node_cls, NODE_IMPL_MARK).values())
        if node_cls is not BaseNode and issubclass(node_cls, BaseNode):
            impls |= get_impls_with_return_type(get_impls_by_key(BaseNode, NODE_IMPL_MARK).values())
        setattr(node_cls, "__node_impls__", impls)
    return getattr(node_cls, "__node_impls__")


class ComposeError(BaseException):
    pass


class Node(abc.ABC):
    node: str = "node"
    scope: NodeScope = NodeScope.PER_EVENT

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @classmethod
    async def compose_annotation(
        cls,
        annotation: typing.Any,
        update: UpdateCute,
        ctx: Context,
    ) -> typing.Any:
        orig_annotation = typing.get_origin(annotation) or annotation
        n_impl = cls.get_node_impls().get(orig_annotation)
        if n_impl is None:
            raise ComposeError(f"Node implementation for compose annotation {annotation!r} not found.")

        result = n_impl(
            cls,
            **magic_bundle(
                n_impl,
                {"update": update, "context": ctx},
                start_idx=0,
                bundle_ctx=False,
            ),
        )
        if inspect.isawaitable(result):
            return await result
        return result

    @classmethod
    def compose_error(cls, error: str | None = None) -> typing.NoReturn:
        raise ComposeError(error)

    @classmethod
    def get_sub_nodes(cls) -> dict[str, type["Node"]]:
        return get_nodes(cls.compose)

    @classmethod
    def get_compose_annotations(cls) -> dict[str, typing.Any]:
        return get_compose_annotations(cls.compose)

    @classmethod
    def get_node_impls(cls) -> dict[typing.Any, typing.Callable[..., typing.Any]]:
        return get_node_impls(cls)

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> bool:
        return is_generator(cls.compose)


class BaseNode(Node, abc.ABC):
    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @node_impl
    def compose_api(cls, update: UpdateCute) -> API:
        return update.ctx_api

    @node_impl
    def compose_context(cls, context: Context) -> Context:
        return context

    @node_impl
    def compose_update(cls, update: UpdateCute) -> UpdateCute:
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
            },
        )

    class ScalarNode(ScalarNodeProto, abc.ABC, metaclass=create_class):
        pass


__all__ = (
    "BaseNode",
    "ComposeError",
    "DataNode",
    "Node",
    "SCALAR_NODE",
    "ScalarNode",
    "ScalarNodeProto",
    "get_compose_annotations",
    "get_nodes",
    "is_node",
)
