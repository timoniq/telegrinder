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
from telegrinder.node.payload import PayloadData
from telegrinder.rules import (
    CallbackDataEq,
    CallbackDataMarkup,
    PayloadModelRule,
    Text,
)
from telegrinder.tools import MsgPackSerializer

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("DEBUG")


@dataclasses.dataclass(slots=True, frozen=True)
class Item:
    __key__ = "item"

    name: str
    amount: int = dataclasses.field(kw_only=True)


item_serializer = MsgPackSerializer(Item)
kb = (
    InlineKeyboard()
    .add(InlineButton("Confirm", callback_data="confirm/action"))
    .row()
    .add(InlineButton("One", callback_data="number/1"))
    .add(InlineButton("Two", callback_data="number/2"))
    .row()
    .add(InlineButton("🍎", callback_data=Item("apple", amount=10), callback_data_serializer=item_serializer))
    .add(
        InlineButton("🍌", callback_data=Item("banana", amount=20), callback_data_serializer=item_serializer),
    )
    .row()
    .add(InlineButton("Won't respond", callback_data="number/foobar"))
).get_markup()


@bot.on.message(Text("/action"))
async def action(m: Message):
    await m.answer("Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query(is_blocking=False)
async def handle_fruit_item(item: PayloadData[Item, MsgPackSerializer[Item]]):
    logger.info("Got fruit item={!r}", item)


@bot.on.callback_query(CallbackDataEq("confirm/action"))
async def callback_confirm_handler(cb: CallbackQuery):
    await cb.answer("Okay! Confirmed.")
    await cb.edit_text(text="Action happens.")
    # *some action happens*


@bot.on.callback_query(CallbackDataMarkup("number/<n:int>"))
async def callback_number_handler(cb: CallbackQuery, n: int):
    await cb.answer("{0} + (7 * 6) - {0} = 42🤯🤯🤯".format(n))


@bot.on.callback_query(PayloadModelRule(Item, serializer=MsgPackSerializer, alias="item"))
async def select_item(cb: CallbackQuery, item: Item):
    await cb.answer(f"You ate an {item.name!r} for {item.amount} cents 😋")


bot.run_forever()
