import random

from telegrinder import (
    MESSAGE_IN_CHAT,
    CallbackQuery,
    Checkbox,
    Dispatch,
    Message,
    MessageReplyHandler,
    WaiterMachine,
)
from telegrinder.bot.dispatch.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE
from telegrinder.rules import (
    FuzzyText,
    HasText,
    IntegerInRange,
    PayloadEqRule,
    PayloadMarkupRule,
    Text,
)
from telegrinder.tools.formatting import HTMLFormatter, block_quote, link
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard

dp = Dispatch()
wm = WaiterMachine(dp)


kb = (
    InlineKeyboard()
    .add(InlineButton("✅ Confirm", callback_data="action/confirm"))
    .row()
    .add(InlineButton("🛰 Webhook", callback_data="action/webhook"))
    .add(InlineButton("✍️ Quote", callback_data="action/quote"))
    .add(InlineButton("🎲 Guess the number", callback_data="action/guess"))
    .row()
    .add(InlineButton("🐌 Magicoolitka", url="https://magicoolitka.com"))
    .row()
    .add(InlineButton("❌ Cancel", callback_data="action/cancel"))
).get_markup()


@dp.message(Text("/start") | FuzzyText("hello"))
async def start(message: Message) -> None:
    me = (await message.ctx_api.get_me()).unwrap().full_name
    await message.answer(f"Hello, {message.from_user.full_name}, im {me} and i work on a webhook server!")


@dp.message(Text("/cars"))
async def car_choice(message: Message) -> None:
    picked, m_id = await (
        Checkbox(wm, message.chat.id, "🚘 Choose no more than three cars", max_in_row=2)
        .add_option("bentley", "Bentley Continental", "Continental 🤍")
        .add_option("mazda", "Mazda rx 7", "Mazda rx 7 🩵")
        .add_option("toyota", "Toyota Supra mk5", "Supra mk5 💜")
        .wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api)
    )
    await message.edit(
        "🚘 You picked: {}.".format(", ".join(c for c in picked if picked[c])),
        message_id=m_id,
    )


@dp.message(Text("/menu"))
async def handle_menu_command(message: Message) -> None:
    await message.answer("📋 Menu:", reply_markup=kb)


@dp.callback_query(PayloadEqRule("action/webhook"))
async def handle_query_webhook(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.ctx_api.send_message(
        text=HTMLFormatter(
            link(
                "https://core.telegram.org/bots/webhooks",
                "🛰 Marvin's Marvellous Guide to All Things Webhook.",
            )
        ),
        chat_id=cb.chat_id.unwrap(),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


@dp.callback_query(PayloadEqRule("action/quote"))
async def handle_query_quote(cb: CallbackQuery) -> None:
    await cb.answer()
    message = (
        await cb.ctx_api.send_message(
            text="✍️ Send me any message and i'll quote it!",
            chat_id=cb.chat_id.unwrap(),
        )
    ).unwrap()
    msg, _ = await wm.wait(
        MESSAGE_IN_CHAT,
        message.chat.id,
        release=HasText(),
        on_miss=MessageReplyHandler("Im still waiting for your message!"),
    )
    await msg.reply(HTMLFormatter(block_quote(msg.text.unwrap())), parse_mode=HTMLFormatter.PARSE_MODE)


@dp.callback_query(PayloadEqRule("action/guess"))
async def handle_query_guess(cb: CallbackQuery) -> None:
    await cb.answer()
    message = (
        await cb.ctx_api.send_message(
            text="🎲 Okay, i guessed a number between 1 and 10!",
            chat_id=cb.chat_id.unwrap(),
        )
    ).unwrap()
    msg, _ = await wm.wait(
        MESSAGE_IN_CHAT,
        message.chat.id,
        release=IntegerInRange(range(1, 11)),
        on_miss=MessageReplyHandler("Send a number between 1 and 10!"),
    )
    random_number = random.randint(1, 10)
    if int(msg.text.unwrap()) == random_number:
        await msg.answer("🎲 Yayyyyy you guessed it!")
        return
    await msg.answer(f"🎲 Ohh noooo...  i guessed the number {random_number} :-(")


@dp.callback_query(PayloadMarkupRule("action/<action>"))
async def handle_query_action(cb: CallbackQuery, action: str) -> None:
    await cb.answer("✅" if action == "confirm" else "❌")
    match action:
        case "confirm":
            await cb.edit_text("✅ Confirmed!")
        case "cancel":
            await cb.delete()
