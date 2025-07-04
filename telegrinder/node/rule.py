import dataclasses
import typing

from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, Node

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.process import check_rule
    from telegrinder.bot.rules.abc import ABCRule
else:

    def check_rule(*args, **kwargs):
        from telegrinder.bot.dispatch.process import check_rule

        return check_rule(*args, **kwargs)


class RuleChain(dict[str, typing.Any], Node):
    dataclass: type[typing.Any] = dict
    rules: tuple["ABCRule", ...] = ()

    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ == "_RuleNode":
            return
        cls.dataclass = cls.generate_node_dataclass(cls)

    def __new__(cls, *rules: "ABCRule") -> type[Node]:
        return type("_RuleNode", (cls,), {"dataclass": dict, "rules": rules})  # type: ignore

    def __class_getitem__(cls, items: "ABCRule | tuple[ABCRule, ...]", /) -> typing.Self:
        if not isinstance(items, tuple):
            items = (items,)
        return cls(*items)

    @staticmethod
    def generate_node_dataclass(cls_: type["RuleChain"]):  # noqa: ANN205
        return dataclasses.dataclass(type(cls_.__name__, (object,), dict(cls_.__dict__)))

    @classmethod
    async def compose(cls, update: UpdateCute) -> typing.Any:
        ctx = Context()
        for rule in cls.rules:
            if not await check_rule(update.api, rule, update, ctx):
                raise ComposeError(f"Rule {rule!r} failed!")

        try:
            if dataclasses.is_dataclass(cls.dataclass):
                return cls.dataclass(**{k: ctx[k] for k in cls.__annotations__})
            return cls.dataclass(**ctx)
        except Exception as exc:
            raise ComposeError(f"Dataclass validation error: {exc}")

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> typing.Literal[False]:
        return False


__all__ = ("RuleChain",)
