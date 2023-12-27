from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot import ReturnContext
from telegrinder.modules import logger
from telegrinder.rules import Argument, Command, IsPrivate

logger.set_level("INFO")
api = API(Token.from_env())
bot = Telegrinder(api)


def int_validator(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None


@bot.on.message(Command("get", Argument("count", validators=[int_validator])))
async def handler_command_get(message: Message, count: int) -> str:
    return f"You got {count} items."


@bot.on.message(Command("me"))
async def handler_command_me(message: Message) -> list[str]:
    return [
        "First name:",
        message.from_user.first_name,
        "Last name:",
        message.from_user.last_name.unwrap_or("Unknown"),
        "ID:",
        str(message.from_user.id)
    ]


@bot.on.message(Command("secret", Argument("code", validators=[int_validator])), is_blocking=False)
async def handler_command_secret(message: Message, code: int) -> ReturnContext:
    await message.answer("The secret code has been created!")
    return ReturnContext(secret_code=code)


@bot.on.message(IsPrivate())
async def handler_secret_code(message: Message, secret_code: int | None = None):
    if secret_code is None:
        return
    return f"Hey! Secret code: {secret_code!r}"


bot.run_forever()
