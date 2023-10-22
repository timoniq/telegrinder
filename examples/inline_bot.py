import logging

from telegrinder import API, InlineQuery, Telegrinder, Token
from telegrinder.rules import InlineQueryText
from telegrinder.types import InlineQueryResultArticle, InputMessageContent

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)


@bot.on.inline_query(InlineQueryText("test"))
async def test_inline(q: InlineQuery):
    await q.answer(
        results=[
            InlineQueryResultArticle(
                type="article",
                id=1,
                title="Press me",
                input_message_content=InputMessageContent(
                    message_text="I tested inline query",
                ),
            ),
        ]
    )


@bot.on.inline_query()
async def reverse_inline(q: InlineQuery):
    if not q.query:
        return
    await q.answer(
        results=[
            {
                "type": "article",
                "id": "1",
                "title": "Send reversed",
                "input_message_content": dict(message_text=q.query[::-1]),
            }
        ]
    )


bot.run_forever()
