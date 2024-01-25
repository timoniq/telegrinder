from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.result import RESULT_ERROR_LOGGER
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)

RESULT_ERROR_LOGGER.set_log(logger.error)
logger.set_level("INFO")


@bot.on.message(Text("/error"))
async def handle_cancel(m: Message):
    await api.send_message(m.chat.id, text="")


bot.run_forever()
