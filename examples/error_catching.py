from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import configure_dotenv, setup_logger
from telegrinder.node import Error
from telegrinder.rules import IsUser, Text

configure_dotenv()
setup_logger()

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(Text("oops"))
async def oops_handler(m: Message):
    await m.answer("Oh no")
    raise RuntimeError("Wow")


@bot.on.message(Text("woops"))
def woops_handler():
    raise ValueError("Wow oopsii!")


@bot.on.event_error(IsUser())
async def error_handler(err: Error[RuntimeError, ValueError], m: Message):
    await m.answer(f"okay..( Something happened: {err.exception}")


bot.run_forever()
