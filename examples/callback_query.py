import dataclasses
import typing

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
    PayloadEqRule,
    PayloadMarkupRule,
    PayloadModelRule,
    Text,
)
from telegrinder.tools.callback_data_serialization import MsgPackSerializer

api = API(token=Token.from_env())
bot = Telegrinder(api)


@dataclasses.dataclass(slots=True, frozen=True)
class Item:
    __key__ = "item"
    __serializer__ = MsgPackSerializer[typing.Self]

    name: str
    amount: int = dataclasses.field(kw_only=True)


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
async def action(m: Message) -> None:
    await m.answer("Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query(final=False)
async def handle_fruit_item(item: PayloadData[Item]) -> None:
    logger.info("Got fruit item={!r}", item)


@bot.on.callback_query(PayloadEqRule("confirm/action"))
async def callback_confirm_handler(cb: CallbackQuery) -> None:
    await cb.answer("Okay! Confirmed.")
    await cb.edit_text(text="Action happens.")
    # *some action happens*


@bot.on.callback_query(PayloadMarkupRule("number/<n:int>"))
async def callback_number_handler(cb: CallbackQuery, n: int) -> None:
    await cb.answer("{0} + (7 * 6) - {0} = 42🤯🤯🤯".format(n))


@bot.on.callback_query(PayloadModelRule(Item, alias="item"))
async def select_item(cb: CallbackQuery, item: Item) -> None:
    await cb.answer(f"You ate an {item.name!r} for {item.amount} cents 😋")


bot.run_forever()
