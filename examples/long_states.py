import enum

from telegrinder import API, MemoryStateStorage, Message, StateData, StateMeta, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
states = MemoryStateStorage()

logger.set_level("INFO")


class StateEnum(enum.StrEnum):
    # You can't get blessed when cursed,
    # but you can get cursed when blessed...
    CURSED = "cursed"
    BLESSED = "blessed"


@bot.on.message(
    Text("/curse"),
    states.State(StateEnum.BLESSED) | states.State(StateMeta.NO_STATE),
)
async def curse_handler(m: Message):
    await states.set(m.from_user.id, StateEnum.CURSED, {})
    await m.answer("You are now cursed..")


@bot.on.message(
    Text("/bless"),
    states.State(StateMeta.NO_STATE),
)
async def bless_handler(m: Message):
    await states.set(m.from_user.id, StateEnum.BLESSED, {})
    await m.answer("YAS you are now blessed")


@bot.on.message()
async def any_message_handler(m: Message):
    state = await states.get(m.from_user.id)  # TODO: state node
    vibe = state.unwrap_or(StateData("normal", {})).key
    await m.answer(f"Omg you are so {vibe}..")


bot.run_forever()
