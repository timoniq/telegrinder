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
from telegrinder.modules import logger
from telegrinder.rules import CallbackDataMsgPackModel, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


# Alternative to msgspec.Struct: use @dataclasses.dataclass decorator
class ItemModel(msgspec.Struct):
    item: str
    amount: int
    action: str


kb = (
    InlineKeyboard()
    .add(
        InlineButton(
            text="buy a doughnut", callback_data=ItemModel(item="doughnut", amount=100, action="buy")
        )
    )
    .add(InlineButton(text="buy a cake", callback_data=ItemModel(item="cake", amount=1000, action="buy")))
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer(
        text="Hello! Choose what you need:",
        reply_markup=kb,
    )


@bot.on.callback_query(CallbackDataMsgPackModel(ItemModel))
async def buy(cb: CallbackQuery, data: ItemModel):
    await cb.edit_text(f"You bought a {data.item} for {data.amount}")


bot.run_forever()
