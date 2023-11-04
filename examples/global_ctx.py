import time

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import IsPrivate, Text
from telegrinder.tools.global_context import GlobalContext

logger.set_level("INFO")
bot = Telegrinder(API(Token.from_env()))
global_ctx = GlobalContext(
    formatting=False,
    time=int(time.time()),
)


@bot.on.message(IsPrivate(), Text("/formatting"))
async def formatting(m: Message):
    formatting_status = (
        global_ctx.get("formatting", bool).map(lambda x: x.value).unwrap_or(False)
    )
    global_ctx.formatting = not formatting_status
    await m.answer("Formatting " + ("enable!" if global_ctx.formatting else "disable!"))


@bot.on.message(IsPrivate(), Text("/update_time"))
async def show_me(m: Message):
    global_ctx.time = m.date
    await m.reply("Time updated!")


@bot.on.message(IsPrivate(), Text("/clear_ctx"))
async def clear_ctx(m: Message):
    if global_ctx:
        global_ctx.clear()
        await m.reply("Successful ctx cleanup!")
    else:
        await m.answer("Ctx is empty, cant clear it.")


bot.run_forever()
