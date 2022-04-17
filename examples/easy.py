from telegrinder import Telegrinder, API, Token
from telegrinder.bot.rules import Text, Markup
import logging

api = API(token=Token("..."))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on_message(Text("/start"))
async def start(event: dict):
    message = event["message"]
    me = (await api.request("getMe")).unwrap().get("first_name")
    await api.request(
        "sendMessage",
        {
            "chat_id": message["chat"]["id"],
            "text": "Hello, {}! It's {}.".format(message["from"]["first_name"], me),
        },
    )


@bot.on_message(Markup("/reverse <text>"))
async def reverse(event: dict, text: str):
    message = event["message"]
    await api.request(
        "sendMessage",
        {
            "chat_id": message["chat"]["id"],
            "text": f"Okay, its.. {text[-1].upper()}.. {text[-2].upper()}.. {text[::-1].lower().capitalize()}",
        },
    )
    if text[::-1].lower().replace(" ", "") == text.lower().replace(" ", ""):
        await api.request(
            "sendMessage",
            {
                "chat_id": message["chat"]["id"],
                "text": "Wow.. Seems like this is a palindrome.",
            },
        )


bot.run_forever()
