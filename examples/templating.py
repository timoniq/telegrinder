import dataclasses
import pathlib

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text

from telegrinder_templating import JinjaTemplating

jt = JinjaTemplating(pathlib.Path(__file__).resolve().parent / "assets/templates")
bot = Telegrinder(API(Token.from_env()))


@dataclasses.dataclass(frozen=True)
class Command:
    name: str
    description: str = dataclasses.field(kw_only=True)


COMMANDS = [
    Command("start", description="Hello message"),
    Command("help", description="Help reference"),
    Command("ban", description="Ban a user in chat"),
    Command("kick", description="Kick a user from chat"),
    Command("mute", description="Mute a user in chat"),
    Command("stats", description="Chat statistics"),
    Command("adminlist", description="List of administrators in chat"),
]


@bot.on.message(Text("/start"))
async def start_handler(message: Message):
    await message.answer(
        await jt.render(
            "start_template.j2",
            user=message.from_user,
            commands=COMMANDS,
        )
    )


@bot.on.message(Text("/help"))
async def help_handler(message: Message):
    await message.answer(
        await jt.render_from_string(
            """
        It's a help reference!
        Available commands:
        {% for command in commands %}
            {{ loop.index }}. /{{ command.name }}
        {% endfor %}
        """,
            commands=COMMANDS,
        )
    )


bot.run_forever()
