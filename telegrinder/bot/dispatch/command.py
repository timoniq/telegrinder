import dataclasses
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.rules import Markup, Text
from telegrinder.bot.rules.command import Command as CommandRule
from telegrinder.tools.global_context import TelegrinderCtx
from telegrinder.tools.global_context.abc import ABCGlobalContext
from telegrinder.types import Update
from telegrinder.types.enums import UpdateType

from .view.abc import ABCView, FuncType
from .view.message import MessageView

Message: typing.TypeAlias = MessageCute
CmdRule: typing.TypeAlias = Text | Markup | CommandRule


def reveal_command_rule(rule: CmdRule) -> str:
    if isinstance(rule, Text):
        return ", ".join(rule.texts)
    if isinstance(rule, Markup):
        return ", ".join(pattern.text for pattern in rule.patterns)
    if isinstance(rule, CommandRule):
        return ", ".join(" | ".join(p + name for p in rule.prefixes) for name in rule.names) + (
            " - [{}]".format(
                ", ".join(
                    arg.name + ("*" if arg.optional else "")
                    for arg in sorted(rule.arguments, key=lambda a: a.optional)
                )
            )
            if rule.arguments
            else ""
        )


@dataclasses.dataclass
class Command:
    command_rule: CmdRule
    description: str | None = None


@dataclasses.dataclass
class CommandDispatch(ABCDispatch):
    description: str | None = None
    commands: list[Command] = dataclasses.field(default_factory=lambda: [])
    unknown_command_handler: dataclasses.InitVar[ABCHandler[Message] | None] = None
    global_context: ABCGlobalContext = dataclasses.field(default_factory=lambda: TelegrinderCtx())
    message: MessageView = dataclasses.field(
        default_factory=lambda: MessageView(update_type=UpdateType.MESSAGE)
    )

    def __post_init__(self, unknown_command_handler: ABCHandler[Message] | None) -> None:
        if unknown_command_handler is not None:
            self.message.handlers.append(unknown_command_handler)

    def __call__(
        self,
        command: str | list[str] | CmdRule,
        description: str | None = None,
        is_blocking: bool = True,
    ):
        command_rule: CmdRule = Text(command) if isinstance(command, str | list) else command
        self.commands.append(Command(command_rule, description))

        def wrapper(func: FuncType[Message]):
            func_handler = self.message.to_handler(
                command_rule,
                is_blocking=is_blocking,
            )(func)
            self.message.handlers.insert(-1, func_handler)
            return func_handler

        return wrapper

    @property
    def descriptions(self) -> str:
        return "{description}\n\n{commands}".format(
            description=self.description or "",
            commands="\n".join(
                f"{reveal_command_rule(command.command_rule)} — {command.description or ''}"
                for command in self.commands
            ),
        )

    def get_views(self) -> dict[str, ABCView]:
        return {"message": self.message}

    async def feed(self, event: Update, api: ABCAPI) -> bool:
        if await self.message.check(event):
            await self.message.process(event, api)
            return True
        return False

    def load(self, external: typing.Self) -> None:
        self.commands.extend(external.commands)
        self.message.load(external.message)


__all__ = ("Command", "CommandDispatch")
