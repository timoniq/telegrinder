from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger

logger.set_level("INFO")
bot = Telegrinder(API(Token.from_env()))


@bot.on.message()
async def forward_message(message: Message) -> str:
    result = (await message.forward(message.chat_id)).unwrap()
    forward_origin = result.forward_origin.unwrap().v
    text_for_response = "Forwarded message that was sent on {!r} from {}: {!r}"

    match forward_origin.type:
        case "chat":
            return text_for_response.format(
                forward_origin.date.ctime(),
                forward_origin.type,
                forward_origin.sender_chat,
            )
        case "channel":
            return text_for_response.format(
                forward_origin.date.ctime(),
                forward_origin.type,
                forward_origin.chat.title.unwrap(),
            )
        case "hidden_user":
            return text_for_response.format(
                forward_origin.date.ctime(),
                forward_origin.type,
                forward_origin.sender_user_name,
            )
        case "user":
            return text_for_response.format(
                forward_origin.date.ctime(),
                forward_origin.type,
                forward_origin.sender_user.full_name,
            )


bot.run_forever()
