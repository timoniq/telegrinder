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

api = API(Token.from_env())
bot = Telegrinder(api)

wm = WaiterMachine(bot.dispatch)

CANCEL_MARKUP = InlineKeyboard().add(InlineButton("Cancel", callback_data="cancel")).get_markup()


@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    input_message = (await message.answer("Input or cancel", reply_markup=CANCEL_MARKUP)).unwrap()

    hasher, event, _ = await wm.wait_many(
        (CALLBACK_QUERY_FOR_MESSAGE, input_message.message_id),  # type: ignore
        (MESSAGE_FROM_USER, message.from_user.id),  # type: ignore
    )

    if hasher == CALLBACK_QUERY_FOR_MESSAGE:
        await message.answer("Cancel flow")
    else:
        await message.answer(f"Message input: {event.text.unwrap_or('no text')}")  # type: ignore


bot.run_forever()
