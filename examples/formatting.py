from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.tools.formatting import HTMLFormatter, bold, italic, mention

api = API(token=Token.from_env())
api.default_params["parse_mode"] = HTMLFormatter.PARSE_MODE

bot = Telegrinder(api)


@bot.on.message(Text("/formatting"))
async def formatting(m: Message):
    await m.answer(HTMLFormatter(bold(italic("bold italic text!"))))
    await m.answer(
        "python library 'telegrinder' - "
        + HTMLFormatter("{:bold} for effective and reliable telegram {:bold+italic} {:underline}!").format(
            "Framework",
            "bot",
            "building",
        ),
    )
    await m.answer("this is " + mention(m.from_user.first_name, user_id=m.from_user.id))


bot.run_forever()
