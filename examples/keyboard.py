import msgspec

from telegrinder import (
    API,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    StaticButton,
    StaticKeyboard,
    Telegrinder,
    Token,
)
from telegrinder.modules import logger
from telegrinder.rules import PayloadModelRule, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


class FruitsKeyboard(StaticKeyboard, max_in_row=2, one_time_keyboard=True):
    APPLE = StaticButton("🍏 Apple")
    BANANA = StaticButton("Banana 🍌")
    GRAPES = StaticButton("🍇 Grapes")
    KIWI = StaticButton("Kiwi 🥝")


# Alternative to msgspec.Struct: use @dataclasses.dataclass decorator
class ItemModel(msgspec.Struct):
    item: str
    amount: int
    action: str


kb = (
    InlineKeyboard()
    .add(
        InlineButton(
            text="buy a doughnut",
            callback_data=ItemModel(item="doughnut", amount=100, action="buy"),
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


@bot.on.message(Text("/eat"))
async def eat_some_fruit(message: Message) -> None:
    await message.reply(
        text="What fruit do you want to eat?",
        reply_markup=FruitsKeyboard.get_markup(),
    )


@bot.on.message(FruitsKeyboard.APPLE)
async def eat_apple(message: Message) -> None:
    await message.reply(
        text="Very nice green apple, bon appetit!",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )


@bot.on.message(FruitsKeyboard.BANANA)
async def eat_banana(message: Message) -> None:
    await message.reply(
        text="This banana is so ripe and sweet, bon appetit!",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )


@bot.on.message(FruitsKeyboard.GRAPES)
async def eat_grapes(message: Message) -> None:
    await message.reply(
        text="Grapes with seeds, bon appetit!",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )


@bot.on.message(FruitsKeyboard.KIWI)
async def eat_kiwi(message: Message) -> None:
    await message.reply(
        text="Very sour kiwi... Bon appetit!",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )


@bot.on.callback_query(PayloadModelRule(ItemModel))
async def buy(cb: CallbackQuery, data: ItemModel):
    await cb.edit_text(f"You bought a {data.item} for {data.amount}")


bot.run_forever(skip_updates=True)
