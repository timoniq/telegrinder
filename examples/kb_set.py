import dataclasses
import pathlib
import random

from telegrinder import (
    API,
    CallbackQuery,
    InlineKeyboard,
    Keyboard,
    KeyboardSetYAML,
    Message,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.bot.dispatch.handler.message_reply import MessageReplyHandler
from telegrinder.modules import logger
from telegrinder.rules import CallbackDataEq, CallbackDataJsonModel, Text

api = API(token=Token.from_env())
bot = Telegrinder(api=api)
wm = WaiterMachine()

logger.set_level("INFO")


@dataclasses.dataclass
class Item:
    name: str
    cost: int


class KeyboardSet(KeyboardSetYAML):
    __config__ = pathlib.Path("examples") / "assets" / "kb_set_config.yaml"

    KEYBOARD_MENU: Keyboard
    KEYBOARD_YES_NO: Keyboard
    KEYBOARD_ITEMS: InlineKeyboard


@bot.on.message(Text("/menu"))
async def menu_handler(m: Message):
    await m.answer(
        text="You are in menu",
        reply_markup=KeyboardSet.KEYBOARD_MENU.get_markup(),
    )


@bot.on.message(Text(["/choose", "Choose"]))
async def choose_handler(m: Message):
    await m.answer(
        text="Do you like making important decisions?",
        reply_markup=KeyboardSet.KEYBOARD_YES_NO.get_markup(),
    )
    answer, _ = await wm.wait(
        bot.dispatch.message,
        m,
        Text(["yes", "no"], ignore_case=True),
        default=MessageReplyHandler("Please make a decision: Yes or No. This is extremely important!"),
    )
    if answer.text.unwrap().lower() == "yes":
        await answer.reply("Rockets have been launched.")
    else:
        await answer.reply(":(( maybe you need some psychological help")


@bot.on.message(Text(["/choose", "choose"]))
async def choose_item_handler(m: Message):
    await m.answer(
        text="You can choose the inline button below:",
        reply_markup=KeyboardSet.KEYBOARD_ITEMS.get_markup(),
    )


@bot.on.callback_query(CallbackDataEq("remove_kb"))
async def edit_callback_handler(cb: CallbackQuery):
    await cb.answer("Yay")
    chars = list(cb.message.unwrap().only().unwrap().text.unwrap())
    random.shuffle(chars)
    await cb.edit_text("".join(chars))


@bot.on.callback_query(CallbackDataJsonModel(Item))
async def buy_item(cb: CallbackQuery, data: Item):
    await cb.answer(f"Congratulations! You bought {data.name!r} for {data.cost}$")


@bot.on.message(Text("/nokeyboard"))
async def no_keyboard(m: Message):
    await m.answer(
        "No more keyboard",
        reply_markup=KeyboardSet.KEYBOARD_MENU.get_empty_markup(),
    )


KeyboardSet.load()
bot.run_forever()
