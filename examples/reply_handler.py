from telegrinder import API, Telegrinder, Token
from telegrinder.bot.dispatch.handler.message_reply import MessageReplyHandler
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


bot.on.message.handlers.extend(
    [
        MessageReplyHandler("Good morning!", Text("/gm")),
        MessageReplyHandler("What do you say?"),
    ]
)

bot.run_forever()
