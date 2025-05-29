from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.node import Error
from telegrinder.rules import IsUser, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.message(Text("oops"))
async def oops_handler(m: Message):
    await m.answer("Oh no")
    raise RuntimeError("Wow")


@bot.on.error(IsUser())
async def runtime_error_handler(err: Error[RuntimeError], m: Message):
    await m.answer(f"okay..( Something happened: {err.exception}")


bot.run_forever()
