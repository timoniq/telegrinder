from telegrinder import Telegrinder, API, Token, Message, CallbackQuery, InlineKeyboard, InlineButton
from telegrinder.bot.rules import Text
import logging

api = API(token=Token("..."))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

kb = (
    InlineKeyboard()
    .add(InlineButton("Confirm", callback_data="confirm/action"))
).get_markup()


@bot.on.message(Text("/action"))
async def action(m: Message):
    await m.answer("Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query()
async def callback_handler(cb: CallbackQuery):
    if cb.data == "confirm/action":
        await cb.answer("Okay! Confirmed.")
        # *some action happens*


bot.run_forever()
