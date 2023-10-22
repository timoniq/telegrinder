import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.tools import HTMLFormatter, bold, italic, mention

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on.message(Text("/formatting"))
async def formatting(m: Message):
    await m.answer(
        HTMLFormatter(bold(italic("bold italic text!"))),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )
    await m.answer(
        "python library 'telegrinder' - "
        + HTMLFormatter(
            "{:bold} for effective and reliable telegram {:bold+italic} {:underline}!"
        ).format("Framework", "bot", "building"),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )
    await m.answer(
        "this is " + mention(m.from_.first_name, m.from_.id),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


bot.run_forever()
