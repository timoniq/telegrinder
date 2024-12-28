from telegrinder import (
    API,
    CALLBACK_QUERY_FOR_MESSAGE,
    MESSAGE_FROM_USER,
    InlineButton,
    InlineKeyboard,
    Message,
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
async def start_handler(message: Message) -> None:
    input_message = (await message.answer("Input or cancel", reply_markup=CANCEL_MARKUP)).unwrap()
    hasher, event, context = await wm.wait_many(
        (CALLBACK_QUERY_FOR_MESSAGE, input_message.message_id),
        (MESSAGE_FROM_USER, message.from_user.id),
    )

    if hasher == CALLBACK_QUERY_FOR_MESSAGE:
        await message.answer("Cancel flow")
    else:
        await message.answer(f"Message input: {event.text.unwrap_or('no text')}")  # type: ignore


bot.run_forever()
