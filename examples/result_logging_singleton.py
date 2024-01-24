import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.result import RESULT_ERROR_LOGGER
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)

RESULT_ERROR_LOGGER.set_log(logging.error)


@bot.on.message(Text("/error"))
async def handle_cancel(m: Message):
    await api.send_message(m.chat.id, "")


bot.run_forever()
