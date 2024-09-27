from telegrinder import API, InlineQuery, Telegrinder, Token
from telegrinder.rules import InlineQueryText
from telegrinder.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
)

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.inline_query(InlineQueryText("test"))
async def test_inline(q: InlineQuery):
    await q.answer(
        InlineQueryResultArticle(
            "Press me",
            InputTextMessageContent(message_text="I tested inline query"),
        ),
    )


@bot.on.inline_query()
async def reverse_inline(q: InlineQuery):
    if not q.query:
        return
    await q.answer(
        InlineQueryResultArticle(
            "Send reversed",
            InputTextMessageContent(message_text=q.query[::-1]),
        ),
    )


bot.run_forever()
