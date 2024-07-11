import pathlib

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import IsInteger, IsPrivate
from telegrinder.tools.formatting import HTMLFormatter, Link

api = API(Token.from_env())
bot = Telegrinder(api)
glossary = pathlib.Path("examples/assets/kaktovik.txt").read_text(encoding="UTF-8")

logger.set_level("INFO")


@bot.on.message(IsInteger())
async def integer_handler(message: Message) -> None:
    integer = int(message.text.unwrap())
    lst = []

    while integer >= 20:
        lst.append(glossary[integer % 20])
        integer = integer // 20

    lst.append(glossary[integer])

    await message.answer("".join(lst[::-1]))


@bot.on.message(IsPrivate())
async def hello_handler(_: Message) -> HTMLFormatter:
    return HTMLFormatter(
        "Write a positive number and I'll translate it to {} numeral",
    ).format(Link("https://en.wikipedia.org/wiki/Kaktovik_numerals", "kaktovik"))


bot.run_forever()
