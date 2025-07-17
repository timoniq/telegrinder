import typing

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.dispatch.action import action
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.text import Text
from telegrinder.node import ChatId, Error, UserId

bot = Telegrinder(API(Token.from_env()))


def is_not_admin() -> typing.NoReturn:
    # some pretty cool logic here...
    raise IsNotAdminError("you are not admin... not like a boss... im so sori 😞")


class IsNotAdminError(Exception):
    pass


class IsAdmin(ABCRule):
    async def check(self, chat_id: ChatId, user_id: UserId) -> bool:
        for chat_member in (await bot.api.get_chat_administrators(chat_id=chat_id)).unwrap():
            if chat_member.v.user.id == user_id and chat_member.v.status in {"creator", "administrator"}:
                return True

        return False


@bot.on.message(Text("im boss"))
@action(is_not_admin).on(~IsAdmin())
async def handler(message: Message) -> None:
    await message.answer("hi boss 😎")


@bot.on.error()
async def handle_not_admin_error(message: Message, e: Error[IsNotAdminError]) -> None:
    await message.answer(str(e.exception))


bot.run_forever(skip_updates=True)
