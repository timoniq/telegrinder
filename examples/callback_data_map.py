from telegrinder import API, CallbackQuery, Message, Telegrinder, Token
from telegrinder.rules import CallbackDataMap, Text
from telegrinder.tools import InlineButton, InlineKeyboard

bot = Telegrinder(API(Token.from_env()))
kb = (
    InlineKeyboard()
    .add(InlineButton("Apple", callback_data={"item": "apple", "cost": 5}))
    .add(InlineButton("Banana", callback_data={"item": "banana", "cost": 15}))
    .add(InlineButton("Pineapple", callback_data={"item": "pineapple", "cost": 30}))
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer("Hello", reply_markup=kb)


@bot.on.callback_query(CallbackDataMap({"item": str, "cost": lambda v: v < 20}))
async def cb_handler(cb: CallbackQuery, item: str, cost: int):
    await cb.answer(f"{item} | {cost}")


bot.run_forever()
