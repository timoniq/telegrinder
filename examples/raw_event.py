from fntypes.co import Some

from telegrinder import (
    API,
    Message,
    MessageReplyHandler,
    Telegrinder,
    Token,
    Update,
    WaiterMachine,
)
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.rules import ABCRule, HasText, Text
from telegrinder.types import MessageReactionUpdated, ReactionEmoji, UpdateType

bot = Telegrinder(API(Token.from_env()))
wm = WaiterMachine()
logger.set_level("INFO")


class ReactionRule(ABCRule[Update]):
    async def check(self, update: Update, ctx: Context) -> bool:
        match update.get_event(MessageReactionUpdated):
            case Some(event) if event.user:
                user = event.user.unwrap()
                message_id = bot.dispatch.global_context.get_value(
                    f"{user.id}:{event.chat.id}", int
                )
                return message_id.unwrap_or_none() == event.message_id
        return False


@bot.on.message(Text("/reaction"))
async def react_message(message: Message):
    await message.reply("Send me message with any text and i'll react it!")
    msg, _ = await wm.wait(
        bot.dispatch.message,
        message,
        HasText(),
        default=MessageReplyHandler("Im still waiting for the message with any text!"),
    )
    await msg.react(ReactionEmoji.HEART_ON_FIRE)
    bot.dispatch.global_context[f"{msg.from_user.id}:{msg.chat.id}"] = msg.message_id


@bot.on.raw_event(UpdateType.CHAT_BOOST)
async def chat_boost(update: Update):
    boosted_chat = update.chat_boost.unwrap().chat
    logger.info(f"User boosted chat (title={boosted_chat.title.unwrap()}, id={boosted_chat.id})")


@bot.on.raw_event(UpdateType.MESSAGE_REACTION, ReactionRule(), dataclass=MessageReactionUpdated)
async def message_reaction(message_reaction: MessageReactionUpdated):
    new_reactions = [
        x.v.emoji.value if x.v.type == "emoji" else "*custom reaction*"
        for x in message_reaction.new_reaction
    ]
    await bot.api.send_message(
        chat_id=message_reaction.chat.id,
        text=f"Wow! You also reacted to this message with reactions: {', '.join(new_reactions)}",
    )


@bot.on.raw_event(UpdateType.EDITED_MESSAGE, dataclass=Message)
async def edited_message(m: Message):
    logger.info(f"User edit message with id: {m.message_id}")


bot.run_forever()
