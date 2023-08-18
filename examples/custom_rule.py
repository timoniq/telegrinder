from telegrinder import Telegrinder, API, Token, Message, MessageRule
from telegrinder.bot import WaiterMachine
from telegrinder.rules import Text
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logging.basicConfig(level=logging.INFO)


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.photo is not None


class HasNicePhoto(MessageRule, requires=[HasPhoto()]):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.photo[0].width > message.photo[0].height


@bot.on.to_handler()
async def not_a_photo(message: Message):
    await message.answer("Waiting for the photo")


@bot.on.message(Text("/chain"))
async def start_handler(m: Message):
    await m.answer("Send me a photo please")
    m, _ = await wm.wait(bot.dispatch.message, m, HasPhoto(), default=not_a_photo)
    await m.reply("Great photo! Chain completed.")


@bot.on.message(HasNicePhoto())
async def nice_photo_handler(m: Message):
    await m.reply("Wow this photo is really nice")


@bot.on.message(HasPhoto())
async def photo_handler(m: Message):
    await m.answer("You have a photo!")


bot.run_forever()
