import dataclasses
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node import Text

from .abc import ABCRule

Validator = typing.Callable[[str], typing.Any | None]


def single_split(s: str, separator: str) -> tuple[str, str]:
    left, *right = s.split(separator, 1)
    return left, (right[0] if right else "")


@dataclasses.dataclass(frozen=True)
class Argument:
    name: str
    validators: list[Validator] = dataclasses.field(default_factory=lambda: [])
    optional: bool = dataclasses.field(default=False, kw_only=True)
    # NOTE: add optional param `description`

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
    ) -> None:
        self.names = [names] if isinstance(names, str) else names
        self.arguments = arguments
        self.prefixes = prefixes
        self.separator = separator
        self.lazy = lazy

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

    def parse_arguments(self, arguments: list[Argument], s: str) -> dict | None:
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

    async def check(self, text: Text, ctx: Context) -> bool:
        text = self.remove_prefix(text)
        if text is None:
            return False

        name, arguments = single_split(text, self.separator)
        if name not in self.names:
            return False

        if not self.arguments:
            return not arguments

        result = self.parse_arguments(list(self.arguments), arguments)
        if result is None:
            return False

        ctx.update(result)
        return True


__all__ = ("Argument", "Command", "single_split")
