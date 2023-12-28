import dataclasses
import inspect
import typing

from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.base import ComposeError, Node, ScalarNode
from telegrinder.node.update import UpdateNode

from .tools.generator import generate

T = typing.TypeVar("T")


class RuleNode(dict):
    dataclass = dict
    rules: tuple[ABCRule, ...] = ()

    @classmethod
    async def compose(cls, update: UpdateNode):
        ctx = {}
        for rule in cls.rules:
            if not await check_rule(update.api, rule, update, ctx):
                raise ComposeError
        try:
            return cls.dataclass(**ctx)  # type: ignore
        except Exception as exc:
            print(exc)
            raise ComposeError(f"Dataclass validation error: {exc}")
    
    @classmethod
    def as_node(cls):
        return cls
    
    @classmethod
    def get_sub_nodes(cls):
        return {"update": UpdateNode}

    @classmethod
    def is_generator(cls):
        return False

    def __new__(cls, *rules: ABCRule) -> type[Node]:
        return type("_RuleNode", (cls,), {"dataclass": dict, "rules": rules})  # type: ignore
    
    def __class_getitem__(cls, item: tuple[ABCRule, ...]) -> "RuleNode":
        if not isinstance(item, tuple):
            item = (item,)
        return cls(*item)
    
    @staticmethod
    def generate_dataclass(cls_):
        return dataclasses.dataclass(type(cls_.__name__, (object,), dict(cls_.__dict__)))
    
    def __init_subclass__(cls) -> None:
        if cls.__name__ == "_RuleNode":
            return
        cls.dataclass = cls.generate_dataclass(cls)
