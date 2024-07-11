import dataclasses
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, Node
from telegrinder.node.update import UpdateNode

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule


class RuleChain(dict[str, typing.Any]):
    dataclass = dict
    rules: tuple["ABCRule", ...] = ()

    @classmethod
    async def compose(cls, update: UpdateNode):
        from telegrinder.bot.dispatch.process import check_rule

        ctx = Context()
        for rule in cls.rules:
            if not await check_rule(update.api, rule, update, ctx):
                raise ComposeError
        try:
            return cls.dataclass(**ctx)  # type: ignore
        except Exception as exc:
            raise ComposeError(f"Dataclass validation error: {exc}")

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def get_sub_nodes(cls) -> dict:
        return {"update": UpdateNode}

    @classmethod
    def is_generator(cls) -> typing.Literal[False]:
        return False

    def __new__(cls, *rules: "ABCRule") -> type[Node]:
        return type("_RuleNode", (cls,), {"dataclass": dict, "rules": rules})  # type: ignore

    def __class_getitem__(cls, items: typing.Union[tuple["ABCRule", ...], "ABCRule"]) -> typing.Self:
        if not isinstance(items, tuple):
            items = (items,)
        assert all(isinstance(rule, "ABCRule") for rule in items), "All items must be instances of 'ABCRule'."
        return cls(*items)

    @staticmethod
    def generate_node_dataclass(cls_: type["RuleChain"]):  # noqa: ANN205
        return dataclasses.dataclass(type(cls_.__name__, (object,), dict(cls_.__dict__)))

    def __init_subclass__(cls) -> None:
        if cls.__name__ == "_RuleNode":
            return
        cls.dataclass = cls.generate_node_dataclass(cls)


__all__ = ("RuleChain",)
