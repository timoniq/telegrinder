from telegrinder import Telegrinder, API, Token
from telegrinder.rules import Text
from telegrinder.bot.dispatch.handler.message_reply import MessageReplyHandler

api = API(token=Token.from_env())
bot = Telegrinder(api)


bot.on.message.handlers.extend(
    [
        MessageReplyHandler("Good morning!", Text("/gm")),
        MessageReplyHandler("What do you say?"),
    ]
)

bot.run_forever()
