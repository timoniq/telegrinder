import asyncio
import enum
import itertools

from telegrinder import (
    API,
    Button,
    Keyboard,
    Message,
    MessageReplyHandler,
    Telegrinder,
    Token,
    WaiterMachine,
)
from telegrinder.modules import logger
from telegrinder.rules import EnumTextRule, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

YesOrNoKeyboard = (Keyboard().add(Button("Yes")).add(Button("No"))).get_markup()

logger.set_level("INFO")


class YesOrNo(enum.Enum):
    YES = "Yes"
    NO = "No"


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer("Do you want some tee?")
    _, ctx = await wm.wait(
        bot.dispatch.message,
        message,
        EnumTextRule(YesOrNo),
        default=MessageReplyHandler("You want, dont you?"),
    )
    if ctx.enum_text == YesOrNo.NO:
        await message.answer("Leee thats sad dat tee is so sweet")
        return
    await message.answer("Yay here is you tee with a nice krendeliok")
    m = (await message.answer("Preparing..")).unwrap()
    queue = itertools.cycle(["🫖🥨", "🥨🤗", "🤗🫖"])
    for _ in range(10):
        msg = next(queue)
        await m.edit(msg)
        await asyncio.sleep(0.5)
    await message.answer("Tee session is over! Goodbye!")


bot.run_forever()
