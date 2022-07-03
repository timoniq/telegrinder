from telegrinder import Telegrinder, API, Token, Message, ABCMessageRule
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


@bot.on.message(HasPhoto())
async def photo_handler(m: Message):
    await m.answer("Nice photo!")


bot.run_forever()
