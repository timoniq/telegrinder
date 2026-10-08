from telegrinder import API, InlineQuery, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import InlineQueryText
from telegrinder.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
)

configure_dotenv()
setup_logger()

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.inline_query(InlineQueryText("test"))
async def test_inline(q: InlineQuery):
    await q.answer(
        InlineQueryResultArticle(
            title="Press me",
            input_message_content=InputTextMessageContent(message_text="I tested inline query"),
        ),
    )


@bot.on.inline_query()
async def reverse_inline(q: InlineQuery):
    if not q.query:
        return
    await q.answer(
        InlineQueryResultArticle(
            title="Send reversed",
            input_message_content=InputTextMessageContent(message_text=q.query[::-1]),
        ),
    )


bot.run_forever()
