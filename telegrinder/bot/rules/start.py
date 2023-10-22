import typing

from .abc import MessageRule
from .is_from import IsPrivate
from .markup import Markup, Message


class StartCommand(
    MessageRule, requires=[IsPrivate(), Markup(["/start <param>", "/start"])]
):
    def __init__(
        self,
        validator: typing.Callable[[str], typing.Any | None] | None = None,
        *,
        param_required: bool = False,
        alias: str | None = None,
    ) -> None:
        self.param_required = param_required
        self.validator = validator
        self.alias = alias

    async def check(self, _: Message, ctx: dict) -> bool:
        param: str | None = ctx.pop("param", None)
        validated_param = (
            self.validator(param) if self.validator and param is not None else param
        )

        if self.param_required and validated_param is None:
            return False

        ctx[self.alias or "param"] = validated_param
        return True
