import typing

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.modules import logger
from telegrinder.rules import Argument, Command, IsPrivate

logger.set_level("INFO")
api = API(Token.from_env())
bot = Telegrinder(api)

T = typing.TypeVar("T")


def int_validator(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None


class MappedValidator(typing.Generic[T]):
    def __init__(self, validator: typing.Callable[[str], T | None]):
        self.validator = validator

    def __call__(self, value: str) -> list[T] | None:
        values = []
        for ch in value:
            val_ch = self.validator(ch)
            if val_ch is None:
                return None
            values.append(val_ch)
        return values


@bot.on.message(Command("get", Argument("count", validators=[int_validator])))
async def command_handler_get(message: Message, count: int) -> str:
    return f"You got {count} items."


@bot.on.message(Command("me"))
async def command_handler_me(message: Message) -> list[str]:
    return [
        "First name:",
        message.from_user.first_name,
        "Last name:",
        message.from_user.last_name.unwrap_or("Unknown"),
        "ID:",
        str(message.from_user.id)
    ]


@bot.on.message(Command("secret", Argument("code", validators=[MappedValidator(int_validator)])), is_blocking=False)
async def command_handler_secret(message: Message, code: list[int]) -> Context:
    await message.answer("The secret code has been created!")
    return Context(secret_code="".join(map(str, code)))


@bot.on.message(IsPrivate())
async def handler_secret_code(message: Message, secret_code: int | None = None):
    if secret_code is None:
        return
    return f"Hey! Secret code: {secret_code!r}"


bot.run_forever()
