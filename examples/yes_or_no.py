import asyncio
import enum
import itertools

from telegrinder import (
    API,
    Message,
    MessageReplyHandler,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.modules import logger
from telegrinder.rules import EnumTextRule, StartCommand

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logger.set_level("INFO")


class YesOrNo(enum.Enum):
    YES = "Yes"
    NO = "No"


@bot.on.message(StartCommand())
async def start(message: Message) -> str | None:
    await message.answer("Do you want some tee?")
    _, ctx = await wm.wait(
        bot.dispatch.message,
        message,
        EnumTextRule(YesOrNo),
        default=MessageReplyHandler("You want, dont you?", as_reply=True),
    )
    if ctx.enum_text == YesOrNo.NO:
        return "Leee thats sad dat tee is so sweet"

    await message.answer("Yay here is you tee with a nice krendeliok")
    m = (await message.answer("Preparing..")).unwrap()
    queue = itertools.cycle(["🫖🥨", "🥨🤗", "🤗🫖"])
    for _ in range(10):
        await m.edit(next(queue))
        await asyncio.sleep(0.5)
    await message.answer("Tee session is over! Goodbye!")


bot.run_forever()
