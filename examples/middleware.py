from telegrinder import Telegrinder, API, Token, Message, ABCMiddleware
from telegrinder.bot.rules import Text, IsChat
import logging

api = API(token=Token("..."))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


class NoBotMiddleware(ABCMiddleware):
    async def pre(self, event: Message, ctx: dict) -> bool:
        return not event.from_.is_bot


@bot.on.message(IsChat(), Text("/testme"))
async def testme(m: Message):
    await m.reply("You are surely not a bot")


bot.dispatch.message.middlewares.append(NoBotMiddleware())
bot.run_forever()

