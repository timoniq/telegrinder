from telegrinder import Telegrinder, API, Token, Message
from telegrinder.rules import Text
from telegrinder.tools import MarkdownFormatter, HTMLFormatter
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)
formatter = MarkdownFormatter


@bot.on.message(Text("/formatting"))
async def formatting(m: Message):
    await m.answer(
        formatter("bold italic").bold().italic()
        + " and "
        + formatter("strike link")
        .link("https://github.com/timoniq/telegrinder")
        .strike(),
        parse_mode=formatter.PARSE_MODE,
    )
    await m.answer(
        "this is " + formatter("mention").mention(m.from_.id),
        parse_mode=formatter.PARSE_MODE,
    )


@bot.on.message(Text("/change"))
async def change(m: Message):
    global formatter
    formatter = HTMLFormatter if formatter == MarkdownFormatter else MarkdownFormatter
    await m.answer(f"Formatter changed to {formatter.__name__}")


bot.run_forever()
