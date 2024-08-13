import typing

from examples.nodes import DB, create_tables
from telegrinder import API, Message, Telegrinder, Token, node
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch import Context
from telegrinder.bot.rules import ABCRule, Markup, Text
from telegrinder.modules import logger
from telegrinder.node import ScalarNode, node_impl

MessageId = typing.NewType("MessageId", int)

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("DEBUG")


class IsChat(ABCRule):
    async def check(self, source: node.Source) -> bool:
        return source.chat.id < 0


class IsAdmin(ABCRule):
    async def check(self, source: node.Source, db: DB, context: Context) -> bool:
        result = await db.execute("select * from admins where telegram_id = ?", (source.from_user.id,))
        context["is_admin"] = True
        return bool(await result.fetchone())


class IncomingMessageId(ScalarNode, int):
    @classmethod
    async def compose(cls, message_id: MessageId) -> MessageId:
        logger.debug("Message with id: {}", message_id)
        return message_id

    # Create node implementation for 'MessageId' annotation in compose method.
    # This node implementation can be found by return type.
    @node_impl
    def compose_message_id(cls, update: UpdateCute) -> MessageId:
        return MessageId(update.message.expect("Update is not a message.").message_id)


async def promote(user_id: int, *, db: DB) -> None:
    await db.execute("insert into admins(telegram_id) values (?) on conflict do nothing", (user_id,))
    await db.commit()


@bot.on.message(IsChat())
async def photo_in_chat_handler(message: Message, p: node.Photo) -> None:
    photo_size = p.sizes[-1]
    await message.answer("Photo ratio H/W: {}".format(photo_size.height / photo_size.width))


@bot.on.message(Text("/message_id"))
async def reply_handler(_: Message, message_id: IncomingMessageId) -> str:
    return f"Your message id: {message_id}"


### Two handlers below require DB node
# DB node is marked with scope = PER_EVENT
# therefore DB node will only be resolved once on event
# If you run this code you will see that connection opening
# and closing is going to happen only once.


@bot.on.message()
async def photo_handler(
    message: Message,
    db: DB,
    photo: node.Photo,
) -> None:
    await message.answer("Got a photo in private message")


@bot.on.message()
async def integer_handler(
    message: Message,
    db: DB,
    i: node.TextInteger,
) -> None:
    await message.answer(f"{i} + 3 = {i + 3}")


@bot.on.message(IsAdmin(), Text("/op"))
async def add_admin_handler(message: Message, db: DB) -> str | None:
    if not message.reply_to_message:
        return "Need reply"
    await promote(message.reply_to_message.unwrap().from_user.id, db=db)
    await message.answer("Done")


@bot.on.message(Markup("/getadmin <token>"))
async def getadmin_handler(message: Message, token: str, db: DB) -> str:
    if token != api.token:
        return "Wrong token"
    await promote(message.from_user.id, db=db)
    return "Done"


@bot.on.message(Text("/amiadmin"), IsAdmin().optional())
async def amiadmin_handler(message: Message, is_admin: bool = False):
    await message.answer("You are " + ("not " if not is_admin else "") + "an admin")


bot.loop_wrapper.lifespan.on_startup(create_tables())
bot.run_forever()
