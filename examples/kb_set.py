import random

from telegrinder import (
    Telegrinder,
    Token,
    API,
    KeyboardSetYAML,
    InlineKeyboard,
    Keyboard,
    Message,
    CallbackQuery,
)
from telegrinder.bot.rules import Text, CallbackDataEq


class KeyboardSet(KeyboardSetYAML):
    __config__ = "assets/kb_set_config.yaml"

    KEYBOARD_MENU: Keyboard
    KEYBOARD_YES_NO: Keyboard
    KEYBOARD_EDIT: InlineKeyboard


KeyboardSet.load()

api = API(token=Token.from_env())
bot = Telegrinder(api=api)


@bot.on.message(Text("/menu"))
async def menu_handler(m: Message):
    await m.answer(
        text="You are in menu", reply_markup=KeyboardSet.KEYBOARD_MENU.get_markup()
    )


@bot.on.message(Text(["/choose", "Choose"]))
async def choose_handler(m: Message):
    await m.answer(
        text="Do you like making important decisions?",
        reply_markup=KeyboardSet.KEYBOARD_YES_NO.get_markup(),
    )
    answer, _ = await bot.on.message.wait_for_message(
        m.chat.id,
        Text(["yes", "no"], True),
        default="Please make a decision: Yes or No. This is extremely important!",
    )
    if answer.text.lower() == "yes":
        await answer.reply("Cool.")
    else:
        await answer.reply("Rockets have been launched.")


@bot.on.message(Text(["/edit", "Edit"]))
async def edit_handler(m: Message):
    await m.answer(
        text="You can push this button and message will change!",
        reply_markup=KeyboardSet.KEYBOARD_EDIT.get_markup(),
    )


@bot.on.callback_query(CallbackDataEq("edit"))
async def edit_callback_handler(cb: CallbackQuery):
    await cb.answer("Yay")
    chars = list(cb.message.text)
    random.shuffle(chars)
    await bot.api.edit_message_text(
        cb.message.chat.id,
        cb.message.message_id,
        text="".join(chars),
        reply_markup=KeyboardSet.KEYBOARD_EDIT.get_markup(),
    )


bot.run_forever()
