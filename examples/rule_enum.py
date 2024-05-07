from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Markup, RuleEnum, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


class CancelOrUsername(RuleEnum[Message]):
    CANCEL = Text("/cancel")
    USERNAME = Markup("@<username>") | Markup("t.me/<username>")


@bot.on.message(CancelOrUsername.USERNAME)
async def handle_username(m: Message, username: str | None = None):
    await m.answer(f"Username: {username}")


@bot.on.message(CancelOrUsername())
async def handle_cancel(m: Message):
    await m.answer("Uoops everything was canceled so sad... I wish it could continue")


bot.run_forever()
