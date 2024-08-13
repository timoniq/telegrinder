from fntypes.variative import Variative

from telegrinder import API, InlineQuery, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import InlineQueryText
from telegrinder.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
)

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.inline_query(InlineQueryText("test"))
async def test_inline(q: InlineQuery):
    await q.answer(
        InlineQueryResultArticle(
            "article",
            "1",
            "Press me",
            Variative(InputTextMessageContent(message_text="I tested inline query")),  # type: ignore
        ),
    )


@bot.on.inline_query()
async def reverse_inline(q: InlineQuery):
    if not q.query:
        return
    await q.answer(
        InlineQueryResultArticle(
            "article",
            "1",
            "Send reversed",
            Variative(InputTextMessageContent(message_text="I tested inline query")),  # type: ignore
        ),
    )


bot.run_forever()
