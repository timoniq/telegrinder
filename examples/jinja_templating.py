import pathlib

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.tools.templating import JinjaTemplating

COMMANDS = ["start", "help", "ban", "kick", "mute", "stats", "adminlist"]
jt = JinjaTemplating(pathlib.Path(__file__).resolve().parent / "assets/templates")
bot = Telegrinder(API(Token.from_env()))


@bot.on.message(Text("/start"))
async def start_handler(message: Message):
    await message.answer(await jt.render("start_template.j2", user=message.from_user))


@bot.on.message(Text("/help"))
async def help_handler(message: Message):
    await message.answer(
        await jt.render_from_string(
            """
        It's a help reference!<br>
        <br>
        Current commands:<br>
        {% for command in commands %}
            {{ loop.index }}. /{{ command }}<br>
        {% endfor %}
        """,
            commands=COMMANDS,
        )
    )


bot.run_forever()
