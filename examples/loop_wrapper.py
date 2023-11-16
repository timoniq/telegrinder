from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text

SECRET_CHAT_ID = 123456789
api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.loop_wrapper.timer(minutes=1)
async def once_eat():
    print("once yum-yum")


@bot.loop_wrapper.timer(seconds=10, repeat=True)
async def repeat_eat():
    print("repeat yum-yum")


async def hello():
    await bot.api.send_message(
        chat_id=SECRET_CHAT_ID,
        text="Hello!!!",
    )


async def bye():
    print("Bye!!!")


@bot.on.message(Text("/test"))
async def test(m: Message):
    await m.reply("test!")


bot.loop_wrapper.on_startup.append(hello())
bot.loop_wrapper.on_shutdown.append(bye())
bot.run_forever()
