from telegrinder import (
    API,
    ABCRule,
    Message,
    Telegrinder,
    Token,
)
from telegrinder.bot import MESSAGE_FROM_USER, WaiterMachine
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)


class HasPhoto(ABCRule):
    async def check(self, message: Message) -> bool:
        return bool(message.photo and message.photo.unwrap())


class HasNicePhoto(ABCRule, requires=[HasPhoto()]):
    async def check(self, message: Message) -> bool:
        return message.photo.unwrap()[0].width > message.photo.unwrap()[0].height


@bot.on.message(Text("/chain"))
async def start_handler(m: Message):
    await m.answer("Send me a photo please")
    m, _ = await wm.wait(
        hasher=MESSAGE_FROM_USER(m.from_user.id),
        release=HasPhoto(),
    )
    await m.reply("Great photo! Chain completed.")


@bot.on.message(HasNicePhoto())
async def dad_photo_handler(m: Message):
    await m.reply("Wow this photo is really nice")


@bot.on.message(HasPhoto())
async def photo_handler(m: Message):
    await m.answer("You have a photo!")


bot.run_forever()
