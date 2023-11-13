import msgspec

from telegrinder import API, CallbackQuery, InlineButton, InlineKeyboard, Message, Telegrinder, Token
from telegrinder.rules import CallbackDataJsonModel, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)

# alternative to msgspec.Struct: use @dataclasses.dataclass
class ItemModel(msgspec.Struct):
    action = "buy"
    item: str
    amount: int


kb = InlineKeyboard()
kb.add(InlineButton(text="buy a doughnut", callback_data=ItemModel(item="doughnut", amount=100)))
kb.add(InlineButton(text="buy a cake", callback_data=ItemModel(item="cake", amount=1000)))


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer(chat_id=message.chat.id, reply_markup=kb.get_markup(), text="Hello! Choose what you need:")


@bot.on.callback_query(CallbackDataJsonModel(ItemModel))
async def buy(event: CallbackQuery, ctx: dict, data: ItemModel):
    if not event.message:
        return
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text=f"You bought a {data.item} for {data.amount}",
    )


bot.run_forever()
