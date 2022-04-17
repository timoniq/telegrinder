from telegrinder import Telegrinder, API, Token
from telegrinder.bot.rules import Text, Markup
from telegrinder.types import Update
import logging

api = API(token=Token("..."))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on_message(Text("/start"))
async def start(event: Update):
    me = (await api.get_me()).unwrap().first_name
    await api.send_message(
        chat_id=event.message.chat.id,
        text="Hello, {}! It's {}.".format(event.message.from_.first_name, me),
    )


@bot.on_message(Markup("/reverse <text>"))
async def reverse(update: Update, text: str):
    await api.send_message(
        chat_id=update.message.chat.id,
        text=f"Okay, its.. {text[-1].upper()}.. {text[-2].upper()}.. {text[::-1].lower().capitalize()}",
    )
    if text[::-1].lower().replace(" ", "") == text.lower().replace(" ", ""):
        await api.send_message(
            chat_id=update.message.chat.id,
            text="Wow.. Seems like this is a palindrome.",
        )


bot.run_forever()
