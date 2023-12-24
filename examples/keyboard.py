import msgspec

from telegrinder import (
    API,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    Telegrinder,
    Token,
)
from telegrinder.rules import CallbackDataJsonModel, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)


# alternative to msgspec.Struct: use @dataclasses.dataclass
class ItemModel(msgspec.Struct):
    item: str
    amount: int
    action: str = "buy"


kb = (
    InlineKeyboard()
    .add(InlineButton(text="buy a doughnut", callback_data=ItemModel(item="doughnut", amount=100)))
    .add(InlineButton(text="buy a cake", callback_data=ItemModel(item="cake", amount=1000)))
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer(
        chat_id=message.chat.id,
        reply_markup=kb,
        text="Hello! Choose what you need:",
    )


@bot.on.callback_query(CallbackDataJsonModel(ItemModel))
async def buy(event: CallbackQuery, data: ItemModel):
    message = event.message.unwrap()
    await api.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=f"You bought a {data.item} for {data.amount}",
    )


bot.run_forever()
