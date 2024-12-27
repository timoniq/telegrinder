from telegrinder import Telegrinder, API, WaiterMachine, Token, Message, InlineKeyboard, InlineButton
from telegrinder import CALLBACK_QUERY_FOR_MESSAGE, MESSAGE_FROM_USER
from telegrinder.rules import Text


api = API(Token.from_env())
bot = Telegrinder(api)

wm = WaiterMachine(bot.dispatch)

CANCEL_MARKUP = InlineKeyboard().add(InlineButton("Cancel")).get_markup()


@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    input_message = (await message.answer("Input or cancel", reply_markup=CANCEL_MARKUP)).unwrap

    hasher, event, _ = await wm.wait_many(
        (CALLBACK_QUERY_FOR_MESSAGE, input_message.message_id),
        (MESSAGE_FROM_USER, message.from_user.id),
    )

    if hasher == CALLBACK_QUERY_FOR_MESSAGE:
        await message.answer("Cancel flow")
    else:
        await message.answer(f"Message input: {event.text.id}")