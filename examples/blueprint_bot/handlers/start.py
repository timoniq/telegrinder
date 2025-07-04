from examples.blueprint_bot.client import wm
from telegrinder import MESSAGE_FROM_USER, Dispatch, Message
from telegrinder.modules import logger
from telegrinder.rules import HasText, Text

dp = Dispatch()


@dp.message(Text("/funnel"))
async def funnel_handler(message: Message):
    await message.answer("What is your favourite colour of thursday evening")
    msg, _ = await wm.wait(MESSAGE_FROM_USER, message.from_user.id, release=HasText())
    await message.answer("Oki")
    logger.info(
        "{}'s favourite colour of thursday evening is {}",
        msg.from_user.first_name,
        msg.text,
    )
    await message.answer("And what is the pattern of the beautiful scarf you wear in the winter nights?")
    msg, _ = await wm.wait(MESSAGE_FROM_USER, message.from_user.id, release=HasText())
    logger.info(
        "{}'s pattern of the winter scarf is {}",
        msg.from_user.first_name,
        msg.text,
    )
    await message.answer("Brilliant")
