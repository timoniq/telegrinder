from telegrinder import (
    API,
    Message,
    MessageReplyHandler,
    MessageRule,
    Telegrinder,
    Token,
)
from telegrinder.bot import Context, WaiterMachine
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logger.set_level("INFO")


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.photo and message.photo.unwrap())


class HasNicePhoto(MessageRule, requires=[HasPhoto()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.photo.unwrap()[0].width > message.photo.unwrap()[0].height


@bot.on.message(Text("/chain"))
async def start_handler(m: Message):
    await m.answer("Send me a photo please")
    m, _ = await wm.wait(
        bot.dispatch.message,
        m,
        HasPhoto(),
        default=MessageReplyHandler("Waiting for the photo", as_reply=True),
    )
    await m.reply("Great photo! Chain completed.")


@bot.on.message(HasNicePhoto())
async def nice_photo_handler(m: Message):
    await m.reply("Wow this photo is really nice")


@bot.on.message(HasPhoto())
async def photo_handler(m: Message):
    await m.answer("You have a photo!")


bot.run_forever()
