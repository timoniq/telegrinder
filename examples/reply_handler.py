from telegrinder import API, Telegrinder, Token
from telegrinder.bot.dispatch.handler.message_reply import MessageReplyHandler
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)


bot.on.message.handlers.extend(
    [
        MessageReplyHandler("Good morning!", Text("/gm")),
        MessageReplyHandler("What do you say?", as_reply=True),
    ]
)

bot.run_forever()
