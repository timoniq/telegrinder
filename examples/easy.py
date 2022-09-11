from telegrinder import Telegrinder, API, Token, Message
from telegrinder.bot.rules import Text, Markup, FuzzyText
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap().first_name
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(message.from_.first_name, me),
    )
    m, _ = await bot.on.message.wait_for_message(message.chat.id)
    if m.text.lower() == "fine":
        await m.reply("Cool!")
    elif m.text.lower() == "bad":
        await m.reply(
            "Oh, i wish i could help you with that. May be some rest will help"
        )


@bot.on.message(Markup("/reverse <text>"))
async def reverse(message: Message, text: str):
    await message.answer(
        text=f"Okay, its.. {text[-1].upper()}.. {text[-2].upper()}.. {text[::-1].lower().capitalize()}",
    )
    if text[::-1].lower().replace(" ", "") == text.lower().replace(" ", ""):
        await message.answer(
            text="Wow.. Seems like this is a palindrome.",
        )


@bot.on.message(FuzzyText("hello"))
async def hello(message: Message):
    await message.reply("Hi!")

bot.run_forever(skip_updates=True)
