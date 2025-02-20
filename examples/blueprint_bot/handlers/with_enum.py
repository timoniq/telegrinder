from telegrinder import MESSAGE_FROM_USER, Dispatch, Message, MessageReplyHandler
from telegrinder.bot.rules.message import MessageRule
from telegrinder.modules import logger
from telegrinder.rules import HasText, Markup, RuleEnum, Text

from .client import wm  # type: ignore

dp = Dispatch()


class Commands(RuleEnum):
    PLAY = Text(["/play", "/game"])
    GET_PRESENTS = Text("/get_presents")
    COMMIT_SUICIDE = Markup(["/suicide", "/suicide <reason>"])


class WasNaughty(MessageRule, requires=[HasText()]):
    async def check(self, message: Message) -> bool:
        await message.answer("Ok, but were you naughty this year?")
        m, _ = await wm.wait(
            MESSAGE_FROM_USER,
            message.from_user.id,
            release=Text(["yes", "no"], ignore_case=True),
            on_miss=MessageReplyHandler("Yes or no? Were you naughty??"),
        )
        return m.text.unwrap().lower() == "yes"


# The enumeration will only resolve once and save the state in context
dp.message.auto_rules = Commands()


@dp.message(Commands.PLAY)
async def handle_play(m: Message):
    logger.info("Playing ^_^")
    await m.answer("What a wonderful play..")


@dp.message(Commands.GET_PRESENTS, WasNaughty())
async def handler_get_presents_if_naughty(m: Message):
    await m.answer(
        "Well, well, well. You were naughty sooo i don't think i can give you some presents.. Only this dubious tomato for now"
    )
    await m.answer("🍅")
    await m.answer("Behave better next year :)")


@dp.message(Commands.GET_PRESENTS)
async def handle_get_presents(m: Message):
    await m.answer("Ho-ho-ho! These are your high quality presents:")
    await m.answer("🥐 (medialuna from argentina)")
    await m.answer("⚙️ wery important detail to fix your life")
    await m.answer("See ya next year!!")


@dp.message(Commands.COMMIT_SUICIDE)
async def handle_commit_suicide(m: Message, reason: str | None = None):
    if reason is None:
        await m.answer("Please specify your reason to do that")
        await wm.wait(MESSAGE_FROM_USER, m.from_user.id, release=HasText())
    await m.answer(
        "Thats a bad reason because nothing in life is final until it's over you know.. There is no reason to live but at the moment you are not knowing the reason you are living despite everything"
    )
