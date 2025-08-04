import asyncio
import enum
import itertools

from telegrinder import (
    API,
    MESSAGE_FROM_USER,
    Message,
    MessageReplyHandler,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.rules import EnumTextRule, StartCommand

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)


class YesOrNo(enum.Enum):
    YES = "Yes"
    NO = "No"


@bot.on.message(StartCommand())
async def start(message: Message) -> str:
    await message.answer("Do you want some tee?")
    _, ctx = await wm.wait(
        MESSAGE_FROM_USER,
        message.from_user.id,
        release=EnumTextRule(YesOrNo),
        on_miss=MessageReplyHandler("You want, dont you?", as_reply=True),
    )
    if ctx.enum_text == YesOrNo.NO:
        return "Leee thats sad dat tee is so sweet"

    await message.answer("Yay here is you tee with a nice krendeliok")

    m = (await message.answer("Preparing..")).unwrap()
    queue = itertools.cycle(["🫖🥨", "🥨🤗", "🤗🫖"])
    for _ in range(10):
        await m.edit(next(queue))
        await asyncio.sleep(0.5)

    return "Tee session is over! Goodbye!"


bot.run_forever()
