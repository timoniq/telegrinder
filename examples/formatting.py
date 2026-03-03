import datetime

from telegrinder import API, Message, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import Text
from telegrinder.tools.formatting.html import HTML, bold, date_time, italic, mention

configure_dotenv()
setup_logger(level="DEBUG")

api = API(token=Token.from_env())
api.default_params["parse_mode"] = HTML.PARSE_MODE

bot = Telegrinder(api)


@bot.on.message(Text("/formatting"))
async def formatting(m: Message):
    await m.answer(bold(italic("bold italic text!")))
    await m.answer(HTML << "this is " << mention(m.from_user.first_name, user_id=m.from_user.id))
    await m.answer(date_time("tomorrow", datetime.datetime.now() + datetime.timedelta(days=1)))


bot.run_forever(skip_updates=True)
