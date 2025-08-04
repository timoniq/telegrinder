import typing

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Argument, Command

T = typing.TypeVar("T")

api = API(Token.from_env())
bot = Telegrinder(api)


def int_validator(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None


@bot.on.message(Command("get", Argument("count", validators=[int_validator])))
async def command_handler_get(count: int) -> str:
    return f"You got {count} items."


@bot.on.message(Command("me"))
async def command_handler_me(message: Message) -> list[str]:
    return [
        "First name:",
        message.from_user.first_name,
        "Last name:",
        message.from_user.last_name.unwrap_or("Unknown"),
        "ID:",
        str(message.from_user.id),
    ]


bot.run_forever()
