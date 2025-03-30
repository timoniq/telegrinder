from telegrinder import (
    API,
    CALLBACK_QUERY_FOR_MESSAGE,
    MESSAGE_FROM_USER,
    CallbackQueryCute,
    InlineButton,
    InlineKeyboard,
    MessageCute,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.rules import Text

CANCEL_MARKUP = InlineKeyboard().add(InlineButton("Cancel", callback_data="cancel")).get_markup()

api = API(Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)


@bot.on.message(Text("/start"))
async def start_handler(message: MessageCute) -> None:
    input_message = (await message.answer("Input or cancel", reply_markup=CANCEL_MARKUP)).unwrap()
    _, event, _ = await wm.wait_many(
        MESSAGE_FROM_USER(message.from_user.id),
        CALLBACK_QUERY_FOR_MESSAGE(input_message.message_id),
    )

    match event:
        case MessageCute():
            await event.answer(f"Message input: {event.text.unwrap_or('no text')}")
        case CallbackQueryCute():
            await event.answer("Cancel flow")


bot.run_forever()
