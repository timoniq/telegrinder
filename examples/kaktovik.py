import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Integer, IsPrivate
from telegrinder.tools.formatting import HTMLFormatter, Link

api = API(Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)

glossary = open("examples/assets/kaktovik.txt", "r", encoding="utf-8").read()


@bot.on.message(Integer())
async def integer_handler(message: Message) -> None:
    integer = int(message.text.unwrap())
    lst = []

    while integer >= 20:
        lst.append(glossary[integer % 20])
        integer = integer // 20

    lst.append(glossary[integer])

    await message.answer("".join(lst[::-1]))


@bot.on.message(IsPrivate())
async def hello_handler(message: Message) -> None:
    await message.answer(
        HTMLFormatter(
            "Write a positive number and I'll translate it to {} numeral"
        ).format(Link("https://en.wikipedia.org/wiki/Kaktovik_numerals", "kaktovik")),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


bot.run_forever()
