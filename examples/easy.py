import random

from telegrinder import Telegrinder, API, Token, Message
from telegrinder.bot import WaiterMachine
from telegrinder.rules import Text, Markup, FuzzyText
from telegrinder.bot.dispatch.handler.message_reply import MessageReplyHandler
import logging
import pathlib

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logging.basicConfig(level=logging.DEBUG)

kitten_bytes = pathlib.Path("assets/kitten.jpg").read_bytes()


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap().first_name
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(
            message.from_user.first_name, me
        ),
    )
    m, _ = await wm.wait(
        bot.dispatch.message,
        message,
        Text(["fine", "bad"], ignore_case=True),
        default=MessageReplyHandler("Fine or bad"),
    )

    match m.text.lower():
        case "fine":
            await m.reply("Cool!")
        case "bad":
            await message.ctx_api.send_photo(
                message.chat.id,
                caption="I'm sorry... You prob need some kitten pictures",
                photo=("kitten.jpg", kitten_bytes),
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


# In order to make argument optional use this trick:
#   1) declare patterns ordered by their broadness
#   2) don't forget to set default value for optional arguments
@bot.on.message(Markup(["/predict", "/predict <thing>"]))
async def predict(message: Message, thing: str | None = None):
    probability_percent = random.randint(0, 100)
    await message.answer(
        f"I predict the probability {thing or 'it'} will happen is {probability_percent}%"
    )


@bot.on.message(FuzzyText("hello"))
async def hello(message: Message):
    await message.reply("Hi!")


bot.run_forever(skip_updates=True)
