from fntypes.result import Error, Ok

from telegrinder import API, ChatJoinRequest, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import HasInviteLink, IsUser

bot = Telegrinder(API(Token.from_env()))
logger.set_level("DEBUG")


@bot.on.chat_join_request(HasInviteLink(), IsUser())
async def approve_user(request: ChatJoinRequest) -> None:
    match await request.approve():
        case Ok(ok) if ok:
            await request.ctx_api.send_message(
                chat_id=request.chat.id,
                text=f"Welcome to the chat {request.chat.title.unwrap()!r}"
                f", {request.from_user.full_name}!",
            )
        case Error(error):
            logger.error(
                "Something went wrong, error: {!r}, user: {}",
                error.error,
                request.from_user.full_name,
            )


bot.run_forever()
