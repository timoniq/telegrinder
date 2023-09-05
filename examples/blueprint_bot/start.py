from telegrinder import Dispatch, Message
from telegrinder.rules import MessageRule, HasText, Text
from telegrinder.modules import logger
from .client import wm

dp = Dispatch()


@dp.message(Text("/funnel"))
async def funnel_handler(message: Message):
    await message.answer("What is your favourite colour of thursday evening")
    msg, _ = await wm.wait(dp.message, message, HasText())
    await message.answer("Oki")
    logger.info(
        "{}'s favourite colour of thursday evening is {}",
        msg.from_user.first_name,
        msg.text,
    )
    await message.answer("And what is the pattern of the beautiful scarf you wear in the winter nights?")
    msg, _ = await wm.wait(dp.message, message, HasText())
    logger.info(
        "{}'s pattern of the winter scarf is {}",
        msg.from_user.first_name,
        msg.text,
    )
    await message.answer("Brilliant")
