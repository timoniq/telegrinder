from telegrinder import API, CommandDispatch, Dispatch, Message, Telegrinder, Token
from telegrinder.bot.rules.command import Argument
from telegrinder.bot.rules.text import HasText
from telegrinder.modules import logger
from telegrinder.rules import Command, Markup
from telegrinder.tools.formatting.html import HTMLFormatter

logger.set_level("INFO")

dp = Dispatch()


@dp.message.to_handler(HasText())
async def unknown_command_handler(message: Message) -> HTMLFormatter:
    return HTMLFormatter(
        "Unknown command {:bold+underline}"
        "\nTry {:bold+underline} for more information."
    ).format(message.text.unwrap(), "/help")


cmd = CommandDispatch(
    description="These commands are supported:",
    unknown_command_handler=unknown_command_handler,
)


def full_validator(value: str) -> bool | None:
    return None if value.lower() != "full" else True
    

@cmd("/help", description="Display this text.")
async def help_command_handler(_: Message) -> str:
    return cmd.descriptions


@cmd("/start", description="Start the bot.")
async def start_command_handler(message: Message) -> None:
    await message.reply("Hello, world!")


@cmd(Markup("/echo <text>"), description="Echo the given text.")
async def echo_command_handler(message: Message) -> None:
    await message.reply(message.text.unwrap())


@cmd(Markup("/caps <text>"), description="Capitalize the given text")
async def caps_command_handler(message: Message, text: str) -> None:
    await message.reply(text.capitalize())


@cmd(
    Command(
        ["me", "profile"],
        Argument(
            "full",
            [full_validator],
            optional=True
        ),
        prefixes=("!", "/"),
    ),
    description="Show you.",
)
async def me_command_handler(message: Message, full: bool = False) -> None:
    if not full:
        await message.reply(
            "ID: {}, fullname: {}".format(message.from_user.id, message.from_user.full_name),
        )
    else:
        await message.reply(
            "ID: {}, fullname: {}, username: {}, language: {}".format(
                message.from_user.id,
                message.from_user.full_name,
                message.from_user.username.unwrap_or("-"),
                message.from_user.language_code.unwrap_or("-"),
            ),
        )


bot = Telegrinder(
    API(Token.from_env()),
    dispatch=cmd,
)
bot.run_forever()
