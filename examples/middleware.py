import logging

from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.rules import IsChat, IsPrivate, Text
from telegrinder.tools import GlobalContext

logging.basicConfig(level=logging.INFO)
api = API(token=Token.from_env())
bot = Telegrinder(api)
global_ctx = GlobalContext(counter=dict())  # Let's imagine a dummy counter


class ContextMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: dict) -> bool:
        counter: dict[int, int] = global_ctx.counter
        counter[event.chat.id] = counter.get(event.chat.id, 0) + 1
        ctx.update({"count": counter[event.chat.id]})
        return True


@bot.on.message(IsChat(), Text("/testme"))
async def testme_in_chat(m: Message):
    await m.reply("You are surely not a bot")


# The variable count will be passed to handler
# only if it is declared in handler function arguments
@bot.on.message(IsPrivate(), Text("/count"))
async def testme_private(m: Message, count: int):
    await m.reply(f"You wrote me {count} messages since my last reload")


bot.on.message.middlewares.append(ContextMiddleware())
bot.run_forever()
