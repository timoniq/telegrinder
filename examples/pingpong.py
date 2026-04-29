from telegrinder import API, Message, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import Text

configure_dotenv()
setup_logger()


api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(Text("/ping"))
async def pong(m: Message):
    await m.answer("Pong")


bot.run_forever()
