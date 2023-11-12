import dataclasses
import logging

from telegrinder import (
    API,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    Telegrinder,
    Token,
)
from telegrinder.rules import (
    CallbackDataEq,
    CallbackDataJsonModel,
    CallbackDataMarkup,
    Text,
)

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@dataclasses.dataclass
class Item:
    name: str
    cost: int = dataclasses.field(default=0, kw_only=True)


kb = (
    InlineKeyboard()
    .add(InlineButton("Confirm", callback_data="confirm/action"))
    .row()
    .add(InlineButton("One", callback_data="number/1"))
    .add(InlineButton("Two", callback_data="number/2"))
    .row()
    .add(InlineButton("🍎", callback_data=Item("apple", cost=10)))
    .add(InlineButton("🍌", callback_data=Item("banana", cost=20)))
    .row()
    .add(InlineButton("Won't respond", callback_data="number/foobar"))
).get_markup()


@bot.on.message(Text("/action"))
async def action(m: Message):
    await m.answer("Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query(CallbackDataEq("confirm/action"))
async def callback_confirm_handler(cb: CallbackQuery):
    await cb.answer("Okay! Confirmed.")
    await cb.edit_text(text="Action happens.")
    # *some action happens*


@bot.on.callback_query(CallbackDataMarkup("number/<n:int>"))
async def callback_number_handler(cb: CallbackQuery, n: int):
    await cb.answer("{0} + (7 * 6) - {0} = 42🤯🤯🤯".format(n))


@bot.on.callback_query(CallbackDataJsonModel(Item))
async def select_item(cb: CallbackQuery, data: Item):
    await cb.answer(f"You ate a {data.name} for {data.cost} cents 😋")


bot.run_forever()
