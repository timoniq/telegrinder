from telegrinder import API, Bot, Message, Token, setup_logger
from telegrinder.node import UserSource
from telegrinder.rules import Magic

setup_logger(level="DEBUG")
bot = Bot(API(Token.from_env()))


@bot.on.message(
    Magic(Message.photo).expect().then(lambda sizes: sizes[-1]).ensure(lambda size: size.width > size.height)
)
async def cine_handler():
    return "cine"


@bot.on.message(Magic(Message.chat.title).expect().then(lambda title: "friend" in title.lower()))
async def friend_chat_handler():
    return "friend chat"


@bot.on.message(Magic(UserSource).ensure(lambda src: src.first_name == "arseny"))
async def user_handler():
    return "hello arseny"


bot.run_forever(skip_updates=True)
