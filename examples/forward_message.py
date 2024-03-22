from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger

logger.set_level("INFO")
bot = Telegrinder(API(Token.from_env()))


@bot.on.message()
async def forward_message(message: Message) -> str:
    result = (await message.forward(message.chat_id)).unwrap()
    forward_origin = result.forward_origin.unwrap().v
    text_response = "Forwarded message that was sent on {!r} from {}: {!r}".format(
        forward_origin.date.ctime(),
        forward_origin.type,
    )

    match forward_origin.type:
        case "chat":
            text_response = text_response.format(
                forward_origin.sender_chat,
            )
        case "channel":
            text_response = text_response.format(
                forward_origin.chat.title.unwrap(),
            )
        case "hidden_user":
            text_response = text_response.format(
                forward_origin.sender_user_name,
            )
        case "user":
            text_response = text_response.format(
                forward_origin.sender_user.full_name,
            )
    
    return text_response


bot.run_forever()
