import pathlib
import random

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot import MESSAGE_FROM_USER_IN_CHAT, WaiterMachine, clear_wm_storage_worker
from telegrinder.bot.dispatch.handler import MessageReplyHandler
from telegrinder.bot.rules.is_from import IsUser
from telegrinder.modules import logger
from telegrinder.node import Me
from telegrinder.rules import FuzzyText, HasText, Markup, Text
from telegrinder.types.objects import InputFile

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)
kitten_bytes = pathlib.Path("examples/assets/kitten.jpg").read_bytes()
logger.set_level("DEBUG")

bot.dispatch.message.auto_rules.append(IsUser())


@bot.on.message(is_blocking=False)
async def handle_message() -> str:
    return "Hello, World!"


@bot.on.message(Text("/start"))
async def start(message: Message, me: Me):
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(
            message.from_user.first_name,
            me.first_name,
        ),
    )
    m, _ = await wm.wait(
        MESSAGE_FROM_USER_IN_CHAT,
        (message.from_user.id, message.chat_id),
        release=Text(["fine", "bad"], ignore_case=True),
        on_miss=MessageReplyHandler("Fine or bad", as_reply=True),
        isolate=True,
        event_key=message.event_key,
    )

    match m.text.unwrap().lower():
        case "fine":
            await m.reply("Cool!")
        case "bad":
            await message.answer_photo(
                InputFile("kitten.jpg", kitten_bytes),
                caption="I'm sorry... You prob need some kitten pictures",
            )


@bot.on.message(Text("/react"))
async def react(message: Message):
    await message.reply("Send me any message...")
    msg, _ = await wm.wait(
        MESSAGE_FROM_USER_IN_CHAT,
        (message.from_user.id, message.chat_id),
        release=HasText(),
        on_miss=MessageReplyHandler("Your message has no text!"),
        isolate=True,
        event_key=message.event_key,
    )
    await msg.react("💋")


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
    await message.answer(f"I predict the probability {thing or 'it'} will happen is {probability_percent}%")


@bot.on.message(FuzzyText("hello"))
async def hello(message: Message):
    await message.reply("Hi!")


bot.loop_wrapper.add_task(clear_wm_storage_worker(wm))
bot.run_forever(skip_updates=True)
