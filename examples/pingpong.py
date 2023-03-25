from telegrinder import Telegrinder, API, Token, Message
from telegrinder.rules import Text
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)


@bot.on.message(Text("/ping"))
async def pong(m: Message):
    await m.answer("Pong")


bot.run_forever()
