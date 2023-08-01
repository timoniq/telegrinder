import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import HasEntities, IsChat, IsPrivate, MessageEntitiesRule
from telegrinder.tools.formatting import HTMLFormatter, mention
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity

api = API(Token("123:TOKEN"))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on.message(IsChat(), MessageEntitiesRule(MessageEntityType.MENTION))
async def handler_mention_me(message: Message, message_entities: list[MessageEntity]):
    my_username = (await api.get_me()).map(lambda me: me.username).unwrap()
    if (
        not my_username
        or my_username
        != message.text[message_entities[0].offset + 1 : message_entities[0].length]
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
            "entities" if len(message.entities) > 1 else "entity",
            ", ".join(map(lambda e: e.type, message.entities)),
        )
    )


bot.run_forever()
