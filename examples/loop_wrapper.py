from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

SECRET_CHAT_ID = 123456789
bot = Telegrinder(API(Token.from_env()))
logger.set_level("INFO")


@bot.loop_wrapper.timer(minutes=1)
async def once_yum():
    print("yum-yum!")


@bot.loop_wrapper.interval(seconds=10)
async def repeat_yum():
    print("repeat yum-yum!!!")


@bot.loop_wrapper.lifespan.on_startup
async def hello():
    await bot.api.send_message(
        chat_id=SECRET_CHAT_ID,
        text="Hello!!!",
    )


@bot.loop_wrapper.lifespan.on_shutdown
async def bye():
    print("Bye!!!")


@bot.on.message(Text("/hello"))
async def hello_handler(m: Message):
    await m.reply("Hello, world!")


bot.run_forever()
