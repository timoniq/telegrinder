from telegrinder import Telegrinder, API, Token, Message, ABCMiddleware
from telegrinder.rules import Text, IsChat, IsPrivate
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

# Let's imagine a dummy counter
counter: dict[int, int] = {}


class ContextMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: dict) -> bool:
        counter[event.chat.id] = counter.get(event.chat.id, 0) + 1
        ctx.update({"count": counter[event.chat.id]})
        return True


@bot.on.message(IsChat(), Text("/testme"))
async def testme_in_chat(m: Message):
    await m.reply("You are surely not a bot")


# The variable count will be passed to handler
# only if it is declared in handler function arguments
@bot.on.message(IsPrivate(), Text("/count"))
async def testme_private(m: Message, count):
    await m.reply(f"You wrote me {count} messages since my last reload")


bot.on.message.middlewares.append(ContextMiddleware())
bot.run_forever()
