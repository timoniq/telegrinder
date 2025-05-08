import pathlib
import random
import typing

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
)
from telegrinder.bot import WaiterMachine
from telegrinder.bot.dispatch.handler import MessageReplyHandler
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules.is_from import IsPrivate, IsUser
from telegrinder.modules import logger
from telegrinder.node import FileId, Me, Photo, UserId, as_node
from telegrinder.rules import (
    CallbackDataEq,
    FuzzyText,
    HasText,
    IsUpdateType,
    Markup,
    Text,
)
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import InputFile

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)
kitten_pic = InputFile.from_path(pathlib.Path("examples/assets/kitten.jpg"))
logger.set_level("DEBUG")

bot.dispatch.message.auto_rules = IsPrivate() & IsUser()


class DummyMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        return True

    async def post(self, event: Message, ctx: Context) -> None:
        return None


@bot.on.message()
async def handle_photo(photo_id: FileId[Photo]) -> str:
    return f"Photo ID: {photo_id}"


@bot.on.message(final=False)
async def handle_message() -> typing.Literal["Hello, World!"]:
    return "Hello, World!"


@bot.on.message(Text("/start"))
async def start(message: Message, me: Me):
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(
            message.from_user.first_name,
            me.first_name,
        ),
    )
    m, _ = await wm.wait(
        MESSAGE_FROM_USER_IN_CHAT,
        (message.from_user.id, message.chat_id),
        release=Text(["fine", "bad"], ignore_case=True),
        on_miss=MessageReplyHandler("Fine or bad", as_reply=True),
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
async def react(message: Message):
    await message.reply("Send me any message...")
    msg, _ = await wm.wait(
        MESSAGE_FROM_USER_IN_CHAT,
        (message.from_user.id, message.chat_id),
        release=HasText(),
        on_miss=MessageReplyHandler("Your message has no text!"),
        lifespan=DummyMiddleware().to_lifespan(message),
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
async def predict(message: Message, thing: str = "it"):
    probability_percent = random.randint(0, 100)
    await message.answer(f"I predict the probability {thing} will happen is {probability_percent}%")


@bot.on.message(FuzzyText("hello"))
async def hello(message: Message):
    await message.reply("Hi!")


@bot.on.message(FuzzyText("freeze"))
async def freeze_handler(message: Message):
    msg = (
        await message.answer(
            "Well ok freezing",
            reply_markup=InlineKeyboard().add(InlineButton("Unfreeze", callback_data="unfreeze")).get_markup(),
        )
    ).unwrap()

    with bot.on.global_middleware.apply_filters(
        source_filter=(as_node(UserId), message.from_user.id, IsUpdateType(UpdateType.CALLBACK_QUERY)),
    ):
        cb, _ = await wm.wait(
            CALLBACK_QUERY_FOR_MESSAGE,
            msg.message_id,
            release=CallbackDataEq("unfreeze"),
        )
        await cb.edit_text("Wow heated!")


bot.run_forever(skip_updates=True)
