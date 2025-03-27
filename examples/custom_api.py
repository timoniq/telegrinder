import typing

from fntypes.co import Error, Ok, Result

from telegrinder import Dispatch, LoopWrapper, Message, Polling
from telegrinder.api import API, Token
from telegrinder.api.error import APIError
from telegrinder.rules import Command
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import User


class DummyAPI(API):
    _cached_me: User | None = None

    async def get_me(self, **other: typing.Any) -> Result[User, APIError]:
        if self._cached_me is None:
            match await super().get_me(**other):
                case Ok(user):
                    self._cached_me = user
                case Error(_) as err:
                    return err
        return Ok(self._cached_me)


api = DummyAPI(token=Token.from_env())
polling = Polling(api=api)
lw = LoopWrapper()
dp = Dispatch()


@dp.raw_event(Command("get_me"), update_type=UpdateType.MESSAGE, dataclass=Message)
async def message_handler(message: Message) -> None:
    me = (await api.get_me()).unwrap()
    await message.reply(
        "Hello, my name is {}, my id is {}".format(
            me.full_name,
            me.id,
        )
    )


async def run_polling() -> None:
    async for updates in polling.listen():
        for update in updates:
            lw.add_task(dp.feed(update, api))


lw.add_task(run_polling())
lw.run()
