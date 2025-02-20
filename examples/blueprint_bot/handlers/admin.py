import sys

from telegrinder import Dispatch, Message
from telegrinder.rules import MessageRule, Text


class IsAdmin(MessageRule):
    async def check(self, message: Message) -> bool:
        return message.from_user.username.unwrap_or_none() == "timoniq"


dp = Dispatch()
dp.message.auto_rules = IsAdmin()


@dp.message(Text("/explode"))
async def explode_handler(message: Message):
    await message.answer("Oops bot exploded =(")
    sys.exit()
