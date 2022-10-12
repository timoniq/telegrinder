from telegrinder import Telegrinder, API, Token, InlineQuery
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)


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
