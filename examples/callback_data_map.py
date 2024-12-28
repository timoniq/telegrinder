from telegrinder import API, CallbackQuery, InlineButton, InlineKeyboard, Message, Telegrinder, Token
from telegrinder.rules import CallbackDataMap, Text

bot = Telegrinder(API(Token.from_env()))
kb = (
    InlineKeyboard()
    .add(InlineButton("Apple", callback_data={"item": "apple", "amount": 5}))
    .add(InlineButton("Banana", callback_data={"item": "banana", "amount": 15}))
    .add(InlineButton("Pineapple", callback_data={"item": "pineapple", "amount": 30}))
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer("Hello, choose something", reply_markup=kb)


@bot.on.callback_query(CallbackDataMap({"item": str, "amount": lambda v: v <= 20}))
async def eat_item(_: CallbackQuery, item: str, amount: int) -> str:
    return f"You chose: {item=}, {amount=}"


bot.run_forever()
