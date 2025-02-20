import time

from fntypes.result import Error, Ok

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.modules import logger
from telegrinder.rules import IsChat, Markup, MessageRule, Text
from telegrinder.types import ChatPermissions

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


class WithReply(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        if not message.reply_to_message:
            await message.reply("You need to reply to someone's message")
            return False
        return True


class IsChatAdmin(MessageRule, requires=[IsChat()]):
    async def check(self, message: Message, ctx: Context) -> bool:
        admins = (await bot.api.get_chat_administrators(chat_id=message.chat.id)).unwrap()
        if message.from_user.id not in (admin.v.user.id for admin in admins if admin.v.user):
            await message.reply("You need to be an admin in this chat")
            return False
        return True


@bot.on.message(Text("/ping"))
async def ping(msg: Message):
    await msg.answer("Pong")


@bot.on.message(Markup(["/mute", "/mute <hours:int>"]), IsChatAdmin(), WithReply())
async def ban(msg: Message, hours: int = 1):
    perms = ChatPermissions()  # no permissions added
    result = await bot.api.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=msg.reply_to_message.unwrap().from_user.id,
        permissions=perms,
        until_date=int(time.time() + hours * 3600),
    )
    match result:
        case Ok(_):
            await msg.reply("Done")
        case Error(e):
            await msg.reply("Something went wrong (code {})".format(e.code))


bot.run_forever(skip_updates=True)
