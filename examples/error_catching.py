from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.node import Error
from telegrinder.rules import IsUser, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("DEBUG")


@bot.on.message(Text("oops"))
async def oops_handler(m: Message):
    await m.answer("Oh no")
    raise RuntimeError("Wow")


@bot.on.message(Text("woops"))
async def woops_handler(m: Message):
    await m.answer("Huh it seems like smth oops is gonna happen now...")
    raise ValueError("Wow oopsii!")


@bot.on.error(IsUser())
async def runtime_error_handler(err: Error[RuntimeError, ValueError], m: Message):
    await m.answer(f"okay..( Something happened: {err.exception}")


bot.run_forever()
