from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.message(Text("/ping"))
async def pong(m: Message):
    await m.answer("Pong")


bot.run_forever()
