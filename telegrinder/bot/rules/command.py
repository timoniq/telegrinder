import typing
import dataclasses

from .abc import Message
from .text import TextMessageRule


Validator = typing.Callable[[str], typing.Any | None]


def single_split(s: str, separator: str) -> tuple[str, str]:
    left, *right = s.split(separator, 1)
    return left, (right[0] if right else "")


@dataclasses.dataclass
class Argument:
    name: str
    validators: list[Validator] = dataclasses.field(default_factory=lambda: [])
    optional: bool = dataclasses.field(default=False, kw_only=True)

    def check(self, data: str) -> typing.Any | None:
        for validator in self.validators:
            data = validator(data)
            if data is None:
                return None
        return data


class Command(TextMessageRule):
    def __init__(
        self,
        names: str | typing.Iterable[str],
        *arguments: Argument,
        prefixes: tuple[str, ...] = ("/",),
        separator: str = " ",
        lazy: bool = False,
    ) -> None:
        if isinstance(names, str):
            names = [names]
        self.names = names
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
        self, arguments: list[Argument], data_s: str, new_s: str, s: str
    ) -> dict | None:
        argument = arguments[0]
        data = argument.check(data_s)

        if data is None and not argument.optional:
            # Failed: Cannot parse required argument
            return None

        elif data is None:
            # Failed to parse argument
            # and it is optional -> skip it
            return self.parse_arguments(arguments[1:], s)

        # Argument is parsed.
        # Continue parsing remaining data with other arguments
        with_argument = self.parse_arguments(arguments[1:], new_s)

        if with_argument is not None:
            return {argument.name: data, **with_argument}

        if not argument.optional:
            # Parsing with other arguments failed
            # and current argument is not optional
            return None

        # Failed to parse other arguments with remaining data
        # -> skip current optional argument, backtrace data
        return self.parse_arguments(arguments[1:], s)

    def parse_arguments(self, arguments: list[Argument], s: str) -> dict | None:
        if not arguments:
            return {} if not s else None

        if self.lazy:
            data_s, new_s = single_split(s, self.separator)
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

    async def check(self, message: Message, ctx: dict) -> bool:
        text = self.remove_prefix(message.text)

        if text is None:
            return False

        name, arguments = single_split(text, self.separator)
        if name not in self.names:
            return False

        if not self.arguments:
            return not arguments

        result = self.parse_arguments(self.arguments, arguments)
        if result is None:
            return False

        ctx.update(result)
        return True
