import dataclasses
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.command import CommandInfo, single_split
from telegrinder.node.me import Me
from telegrinder.node.source import ChatSource
from telegrinder.types.enums import ChatType

type Validator = typing.Callable[[str], typing.Any | None]


@dataclasses.dataclass(frozen=True, slots=True)
class Argument:
    name: str
    validators: list[Validator] = dataclasses.field(default_factory=lambda: [])
    optional: bool = dataclasses.field(default=False, kw_only=True)

    def check(self, data: str) -> typing.Any | None:
        for validator in self.validators:
            data = validator(data)  # type: ignore
            if data is None:
                return None
        return data


class Command(ABCRule):
    def __init__(
        self,
        names: str | typing.Iterable[str],
        *arguments: Argument,
        prefixes: tuple[str, ...] = ("/",),
        separator: str = " ",
        lazy: bool = False,
        validate_mention: bool = True,
        mention_needed_in_chat: bool = False,
        ignore_case: bool = False,
    ) -> None:
        names = [names] if isinstance(names, str) else names
        self.names = [n.lower() for n in names] if ignore_case else names
        self.arguments = arguments
        self.prefixes = prefixes
        self.separator = separator
        self.lazy = lazy
        self.validate_mention = validate_mention
        self.ignore_case = ignore_case

        # if true then we'll check for mention when message is from a group
        self.mention_needed_in_chat = mention_needed_in_chat

    def remove_prefix(self, text: str) -> str | None:
        for prefix in self.prefixes:
            if text.startswith(prefix):
                return text.removeprefix(prefix)
        return None

    def parse_argument(
        self,
        arguments: list[Argument],
        data_s: str,
        new_s: str,
        s: str,
    ) -> dict | None:
        argument = arguments[0]
        data = argument.check(data_s)
        if data is None and not argument.optional:
            return None

        if data is None:
            return self.parse_arguments(arguments[1:], s)

        with_argument = self.parse_arguments(arguments[1:], new_s)
        if with_argument is not None:
            return {argument.name: data, **with_argument}

        if not argument.optional:
            return None

        return self.parse_arguments(arguments[1:], s)

    def parse_arguments(self, arguments: list[Argument], s: str) -> dict[str, typing.Any] | None:
        if not arguments:
            return {} if not s else None

        if self.lazy:
            return self.parse_argument(arguments, *single_split(s, self.separator), s)

        all_split = s.split(self.separator)
        for i in range(1, len(all_split) + 1):
            ctx = self.parse_argument(
                arguments,
                self.separator.join(all_split[:i]),
                self.separator.join(all_split[i:]),
                s,
            )
            if ctx is not None:
                return ctx

        return None

    def check(self, command: CommandInfo, me: Me, chat: ChatSource, ctx: Context) -> bool:
        name = self.remove_prefix(command.name)
        if name is None:
            return False

        target_name = name.lower() if self.ignore_case else name

        if target_name not in self.names:
            return False

        if not command.mention and self.mention_needed_in_chat and chat.type is not ChatType.PRIVATE:
            return False

        if command.mention and self.validate_mention:  # noqa
            if command.mention.unwrap().lower() != me.username.unwrap().lower():
                return False

        if not self.arguments:
            return not command.arguments

        result = self.parse_arguments(list(self.arguments), command.arguments)
        if result is None:
            return False

        ctx.update(result)
        return True


__all__ = ("Argument", "Command", "single_split")
