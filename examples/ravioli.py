import asyncio
import dataclasses
import datetime

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
RAVIOLI_TIME_TO_COOK = 9 * 60

logger.set_level("INFO")


@dataclasses.dataclass
class TimerInfo:
    name: str
    end_time: datetime.datetime
    task: asyncio.Task


class FakeDB:
    def __init__(self) -> None:
        self.storage = {}

    def get(self, user_id: int) -> list[TimerInfo]:
        return self.storage.get(user_id) or []

    def add(self, user_id: int, tinfo: TimerInfo) -> None:
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append(tinfo)

    def new(self, name: str, time: int, message: Message) -> TimerInfo:
        task = asyncio.get_running_loop().create_task(self.timer(name, time, message))
        return TimerInfo(name, datetime.datetime.now() + datetime.timedelta(seconds=time), task)

    async def timer(self, name: str, time: int, message: Message) -> None:
        await asyncio.sleep(time)
        await message.reply(f"{name}'s are ready! Switch off the oven quickly")
        self.storage[message.from_user.id].pop(0)


db = FakeDB()


@bot.on.message(Text("/ravioli"))
async def start(message: Message):
    ravioli = db.new("Ravioli", RAVIOLI_TIME_TO_COOK, message)
    db.add(message.from_user.id, ravioli)
    await message.answer("Timer for ravioli is set!")


@bot.on.message(Text("/cooking"))
async def cooking(message: Message):
    boiling = db.get(message.from_user.id)
    if not boiling:
        await message.answer("Nothing is cooking right now!")
        return
    text = "\n".join(
        "{}. {} will be ready at {}".format(
            i + 1,
            record.name,
            record.end_time,
        )
        for i, record in enumerate(boiling)
    )
    await message.answer("Boiling raviolies:\n\n" + text)


bot.run_forever()
