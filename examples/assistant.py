from telegrinder import Telegrinder, API, Token, Message
from telegrinder.types import ChatPermissions
from telegrinder.bot.rules import Text, Markup, ABCMessageRule, IsChat
import time
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


class WithReply(ABCMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        if not message.reply_to_message:
            await message.reply("You need to reply to someone's message")
            return False
        return True


class IsChatAdmin(ABCMessageRule, require=[IsChat()]):
    async def check(self, message: Message, ctx: dict) -> bool:
        admins = (await bot.api.get_chat_administrators(message.chat.id)).unwrap()
        if message.from_.id not in (admin.user.id for admin in admins):
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
        msg.chat.id,
        msg.reply_to_message.from_.id,
        permissions=perms,
        until_date=int(time.time() + hours * 3600),
    )
    if result.is_ok:
        await msg.reply("Done")
    else:
        await msg.reply("Something went wrong (code {})".format(result.error.code))


bot.run_forever(skip_updates=True)
