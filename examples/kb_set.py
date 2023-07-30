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
    WaiterMachine,
)
from telegrinder.rules import Text, CallbackDataEq
from telegrinder.types import ReplyKeyboardRemove


class KeyboardSet(KeyboardSetYAML):
    __config__ = "examples/assets/kb_set_config.yaml"

    KEYBOARD_MENU: Keyboard
    KEYBOARD_YES_NO: Keyboard
    KEYBOARD_EDIT: InlineKeyboard


KeyboardSet.load()

api = API(token=Token.from_env())
bot = Telegrinder(api=api)
wm = WaiterMachine()


@bot.on.message(Text("/menu"))
async def menu_handler(m: Message):
    await m.answer(
        text="You are in menu", reply_markup=KeyboardSet.KEYBOARD_MENU.get_markup()
    )


@bot.dispatch.to_handler()
async def repeat_yes_or_no(m: Message):
    await m.answer("Please make a decision: Yes or No. This is extremely important!")


@bot.on.message(Text(["/choose", "Choose"]))
async def choose_handler(m: Message):
    await m.answer(
        text="Do you like making important decisions?",
        reply_markup=KeyboardSet.KEYBOARD_YES_NO.get_markup(),
    )
    answer, _ = await wm.wait(
        bot.dispatch.message,
        m,
        Text(["yes", "no"], True),
        default=repeat_yes_or_no,
    )
    if answer.text.lower() == "yes":
        await answer.reply("Rockets have been launched.")
    else:
        await answer.reply(":(( maybe you need some psychological help")


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


@bot.on.message(Text("/nokeyboard"))
async def no_keyboard(m: Message):
    await m.answer(
        "No more keyboard", reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
    )


bot.run_forever()
