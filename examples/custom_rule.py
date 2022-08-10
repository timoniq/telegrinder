from telegrinder import Telegrinder, API, Token, Message, ABCMessageRule
from telegrinder.bot.rules import Text
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


class HasPhoto(ABCMessageRule):
    """
    This is custom rule;
    it should implement asynchronous check method
    """

    async def check(self, message: Message, ctx: dict) -> bool:
        return message.photo is not None


@bot.on.message(Text("/chain"))
async def start_handler(m: Message):
    await m.answer("Send me a photo please")
    m, _ = await bot.dispatch.message.wait_for_message(m.chat.id, HasPhoto(), default="Waiting for the photo")
    await m.reply("Great photo! Chain completed.")


@bot.on.message(HasPhoto())
async def photo_handler(m: Message):
    await m.answer("Nice photo!")


bot.run_forever()
