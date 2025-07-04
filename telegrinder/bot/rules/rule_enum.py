import dataclasses
import typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule, check_rule
from telegrinder.bot.rules.func import FuncRule
from telegrinder.types.objects import Update


@dataclasses.dataclass(slots=True)
class RuleEnumState:
    name: str
    rule: ABCRule
    cls: type["RuleEnum"]

    def __eq__(self, other: typing.Self) -> bool:
        return self.cls == other.cls and self.name == other.name


class RuleEnum(ABCRule):
    __enum__: list[RuleEnumState]

    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        new_attributes = set(cls.__dict__) - set(RuleEnum.__dict__) - {"__enum__", "__init__"}
        enum_lst: list[RuleEnumState] = []

        self = cls.__new__(cls)
        self.__init__()

        for attribute_name in new_attributes:
            rules = getattr(cls, attribute_name)
            attribute = RuleEnumState(attribute_name, rules, cls)

            setattr(
                self,
                attribute.name,
                self & FuncRule(lambda _, ctx: self.must_be_state(ctx, attribute)),  # type: ignore
            )
            enum_lst.append(attribute)

        setattr(cls, "__enum__", enum_lst)

    @classmethod
    def save_state(cls, ctx: Context, enum: RuleEnumState) -> None:
        ctx.update({cls.__name__ + "_state": enum})

    @classmethod
    def check_state(cls, ctx: Context) -> RuleEnumState | None:
        return ctx.get(cls.__name__ + "_state")

    @classmethod
    def must_be_state(cls, ctx: Context, state: RuleEnumState) -> bool:
        real_state = cls.check_state(ctx)
        if not real_state:
            return False
        return real_state == state

    async def check(self, event: Update, api: API, ctx: Context) -> bool:
        if self.check_state(ctx):
            return True

        for enum in self.__enum__:
            ctx_copy = ctx.copy()
            if await check_rule(api, enum.rule, event, ctx_copy):
                ctx.update(ctx_copy)
                self.save_state(ctx, enum)
                return True

        return False


__all__ = ("RuleEnum", "RuleEnumState")
