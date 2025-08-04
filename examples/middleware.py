from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.rules import IsChat, IsPrivate, IsUser, Text
from telegrinder.tools.global_context import GlobalContext

api = API(token=Token.from_env())
bot = Telegrinder(api)
global_ctx = GlobalContext(counter=dict[int, int]())  # Let's imagine a dummy counter


@bot.on.message.register_middleware
class CountMiddleware(ABCMiddleware):
    def pre(self, message: Message, context: Context) -> bool:
        counter = global_ctx.get_value("counter", dict[int, int]).unwrap()
        counter[message.chat.id] = context.count = counter.get(message.chat.id, 0) + 1
        return True


@bot.on.message(IsChat(), IsUser(), Text("/testme"))
async def testme_in_chat(m: Message) -> None:
    await m.reply("You are surely not a bot")


# The variable count will be passed to handler
# only if it is declared in handler function arguments
@bot.on.message(IsPrivate(), Text("/count"))
async def testme_private(count: int) -> str:
    return f"You wrote me {count} messages since my last reload"


bot.run_forever()
