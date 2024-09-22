import dataclasses

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
from telegrinder.node.callback_query import Field
from telegrinder.rules import (
    CallbackDataEq,
    CallbackDataJsonModel,
    CallbackDataMarkup,
    Text,
)

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@dataclasses.dataclass(slots=True, frozen=True)
class Item:
    name: str
    amount: int = dataclasses.field(default=0, kw_only=True)


kb = (
    InlineKeyboard()
    .add(InlineButton("Confirm", callback_data="confirm/action"))
    .row()
    .add(InlineButton("One", callback_data="number/1"))
    .add(InlineButton("Two", callback_data="number/2"))
    .row()
    .add(InlineButton("🍎", callback_data=Item("apple", amount=10)))
    .add(InlineButton("🍌", callback_data=Item("banana", amount=20)))
    .row()
    .add(InlineButton("Won't respond", callback_data="number/foobar"))
).get_markup()


@bot.on.message(Text("/action"))
async def action(m: Message):
    await m.answer("Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query(is_blocking=False)
async def handle_fruit(name: Field[str]):
    logger.info("Got {!r} fruit!", name)


@bot.on.callback_query(CallbackDataEq("confirm/action"))
async def callback_confirm_handler(cb: CallbackQuery):
    await cb.answer("Okay! Confirmed.")
    await cb.edit_text(text="Action happens.")
    # *some action happens*


@bot.on.callback_query(CallbackDataMarkup("number/<n:int>"))
async def callback_number_handler(cb: CallbackQuery, n: int):
    await cb.answer("{0} + (7 * 6) - {0} = 42🤯🤯🤯".format(n))


@bot.on.callback_query(CallbackDataJsonModel(Item, alias="item"))
async def select_item(cb: CallbackQuery, item: Item):
    await cb.answer(f"You ate an {item.name} for {item.amount} cents 😋")


bot.run_forever()
