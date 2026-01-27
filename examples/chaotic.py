import pathlib
import random
from datetime import timedelta
from functools import partial

from telegrinder import (
    API,
    CALLBACK_QUERY_FOR_MESSAGE,
    MESSAGE_FROM_USER_IN_CHAT,
    Context,
    InlineButton,
    InlineKeyboard,
    Message,
    Telegrinder,
    Token,
    configure_dotenv,
    setup_logger,
)
from telegrinder.bot import WaiterMachine
from telegrinder.bot.dispatch.handler import MessageReplyHandler
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.node import Me, UserId
from telegrinder.rules import (
    CallbackDataEq,
    FuzzyText,
    HasText,
    IsUpdateType,
    IsUser,
    Markup,
    Text,
)
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import InputFile

configure_dotenv(load_file=True)
setup_logger(
    level="DEBUG",
    format="<level>{levelname: <8}</level>{module}:{funcName}:{lineno}:<light_white>{message}</light_white>",
)

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()
kitten_pic = InputFile.from_path(pathlib.Path("examples/assets/kitten.jpg"))

bot.dispatch.message.auto_rules = IsUser()


async def on_drop(chat_id: int) -> None:
    await api.send_message(chat_id=chat_id, text="Okay, never mind....")


class DummyMiddleware(ABCMiddleware):
    def pre(self) -> bool:
        return True

    def post(self) -> None:
        return None


@bot.on.message(Text("/start"))
async def start(message: Message, me: Me) -> None:
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(
            message.from_user.first_name,
            me.first_name,
        ),
    )
    m, _ = await wm.wait(
        hasher=MESSAGE_FROM_USER_IN_CHAT(bot.on.message, (message.chat_id, message.from_user.id)),
        release=Text(["fine", "bad"], ignore_case=True),
        lifetime=timedelta(seconds=60),
        on_miss=MessageReplyHandler("Fine or bad", as_reply=True),
        on_drop=partial(on_drop, chat_id=message.chat_id),
    )

    match m.text.unwrap().lower():
        case "fine":
            await m.reply("Cool!")
        case "bad":
            await message.answer_photo(
                photo=kitten_pic,
                caption="I'm sorry... You prob need some kitten pictures",
            )


@bot.on.message(Text("/react"))
async def react(message: Message, context: Context):
    await message.reply("Send me any message...")
    msg, _ = await wm.wait(
        hasher=MESSAGE_FROM_USER_IN_CHAT(bot.on.message, (message.from_user.id, message.chat_id)),
        release=HasText(),
        on_miss=MessageReplyHandler("Your message has no text!"),
        lifespan=DummyMiddleware().to_lifespan(context),
    )
    await msg.react("🔥")


@bot.on.message(Markup("/reverse <text>"))
async def reverse(message: Message, text: str):
    await message.answer(
        text=f"Okay, its.. {text[-1].upper()}.. {text[-2].upper()}.. {text[::-1].lower().capitalize()}",
    )
    if text[::-1].lower().replace(" ", "") == text.lower().replace(" ", ""):
        await message.answer(
            text="Wow.. Seems like this is a palindrome.",
        )


# In order to make argument optional use this trick:
#   1) declare patterns ordered by their broadness
#   2) don't forget to set default value for optional arguments
@bot.on.message(Markup(["/predict", "/predict <thing>"]))
async def predict(thing: str = "it"):
    probability_percent = random.randint(0, 100)
    return f"I predict the probability {thing} will happen is {probability_percent}%"


@bot.on.message(FuzzyText("hello"))
async def hello(message: Message):
    await message.reply("Hi!")


@bot.on.message(FuzzyText("freeze"))
async def freeze_handler(message: Message):
    msg = (
        await message.answer(
            text="Well ok freezing",
            reply_markup=InlineKeyboard().add(InlineButton("Unfreeze", callback_data="unfreeze")).get_markup(),
        )
    ).unwrap()

    with bot.dispatch.middlewares.filter.hold(
        UserId,
        message.from_user.id,
        IsUpdateType(UpdateType.CALLBACK_QUERY),
    ):
        cb, _ = await wm.wait(
            hasher=CALLBACK_QUERY_FOR_MESSAGE(bot.on.callback_query, msg.message_id),
            release=CallbackDataEq("unfreeze"),
        )
        await cb.edit_text("Wow heated!")


bot.run_forever(skip_updates=True)
