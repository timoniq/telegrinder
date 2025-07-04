from fntypes.result import RESULT_ERROR_LOGGER, Error

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

logger.set_level("INFO")
RESULT_ERROR_LOGGER.set_log(logger.error)

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(Text("/error_no_control"))
async def handle_error_no_control(m: Message):
    # This is going to log potentially lost information about api error
    # Here error is not considered to be processed
    await api.send_message(chat_id=m.chat.id, text="")

    # In the following context error is also considered not to be processed
    # because .unwrap_or method omits the error data in the case of Error state of result
    # Thus, nothing is going to be logged
    result = await api.send_message(chat_id=m.chat.id, text="")
    result.unwrap_or(None)


@bot.on.message(Text("/error_controlled"))
async def handle_error_controlled(m: Message):
    # This is not going to log api error traceback because error is being processed with .unwrap()
    # Here error is considered to be processed in the scope we are in
    (await api.send_message(chat_id=m.chat.id, text="")).unwrap()

    # This is going to raise exception
    print("Unreachable code")


@bot.on.message(Text("/error_manually_controlled"))
async def handle_error_manually_controlled(m: Message):
    # This is not going to log api error due to the access (two cases demonstrated) of error field
    # Here error is considered to be processed
    result = await api.send_message(chat_id=m.chat.id, text="")

    # First case, control pass with pattern matching
    match result:
        case Error(err):
            print(err)

    # Second case
    if isinstance(result, Error):
        print(result.error)

    # Thus, no log is going to happen, only two prints out of cases shown above


bot.run_forever()
