from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import HasEntities, IsChat, IsPrivate, MessageEntities
from telegrinder.tools.formatting import HTMLFormatter, mention
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity

api = API(Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.message(IsChat(), MessageEntities(MessageEntityType.MENTION))
async def handler_mention_me(message: Message, message_entities: list[MessageEntity]):
    my_username = (await api.get_me()).map(lambda me: me.username).unwrap()
    if (
        not my_username
        or my_username != message.text.unwrap()[message_entities[0].offset + 1 : message_entities[0].length]
    ):
        return
    await message.delete()
    await message.answer(
        HTMLFormatter("{:bold} don't mention me please!").format(
            mention(
                message.from_user.first_name,
                message.from_user.id,
            )
        ),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


@bot.on.message(IsPrivate(), HasEntities())
async def handler_entities(message: Message):
    await message.answer(
        "Nice {}: {}!".format(
            "entities" if len(message.entities.unwrap()) > 1 else "entity",
            ", ".join(map(lambda e: e.type, message.entities.unwrap())),
        )
    )


bot.run_forever()
