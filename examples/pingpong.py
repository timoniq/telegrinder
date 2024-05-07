from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.cute_types import MessageCute, UpdateCute
from telegrinder.modules import logger
from telegrinder.rules import Text
from telegrinder.types.enums import UpdateType

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("DEBUG")


@bot.on.message(Text("/ping"))
async def pong(m: Message):
    await m.answer("Pong")


@bot.on.raw_event(UpdateType.EDITED_MESSAGE, dataclass=MessageCute)
async def handler(update: MessageCute) -> None:
    print(update)


bot.run_forever()
