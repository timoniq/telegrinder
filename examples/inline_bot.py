from telegrinder import API, InlineQuery, Telegrinder, Token
from telegrinder.bot.cute_types.utils import (
    inline_query_article,
    input_text_message_content,
)
from telegrinder.modules import logger
from telegrinder.rules import InlineQueryText

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.inline_query(InlineQueryText("test"))
async def test_inline(q: InlineQuery):
    await q.answer(
        inline_query_article(
            "1", "Press me", input_text_message_content("I tested inline query")
        )
    )


@bot.on.inline_query()
async def reverse_inline(q: InlineQuery):
    if not q.query:
        return
    await q.answer(
        inline_query_article(
            "1", "Send reversed", input_text_message_content("I tested inline query")
        ),
    )


bot.run_forever()
