from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.modules import logger
from telegrinder.rules import IsChat, IsPrivate, Text
from telegrinder.tools.global_context import GlobalContext

api = API(token=Token.from_env())
bot = Telegrinder(api)
global_ctx = GlobalContext(counter=dict())  # Let's imagine a dummy counter

logger.set_level("INFO")


@bot.on.message.register_middleware()
class ContextMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        counter = global_ctx.get_value("counter", dict[int, int]).unwrap()
        counter[event.chat.id] = counter.get(event.chat.id, 0) + 1
        ctx.set("count", counter[event.chat.id])
        return True


@bot.on.message(IsChat(), Text("/testme"))
async def testme_in_chat(m: Message):
    await m.reply("You are surely not a bot")


# The variable count will be passed to handler
# only if it is declared in handler function arguments
@bot.on.message(IsPrivate(), Text("/count"))
async def testme_private(m: Message, count: int):
    await m.reply(f"You wrote me {count} messages since my last reload")


bot.run_forever()
