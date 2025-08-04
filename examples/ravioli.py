import asyncio
import dataclasses
import datetime

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Markup, Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
RAVIOLI_TIME_TO_COOK = 9 * 60


@dataclasses.dataclass
class TimerInfo:
    name: str
    end_time: datetime.datetime


class DummyDB:
    def __init__(self) -> None:
        self.storage: dict[int, list[TimerInfo]] = {}

    def get(self, user_id: int) -> list[TimerInfo]:
        return self.storage.get(user_id) or []

    def add(self, user_id: int, tinfo: TimerInfo) -> None:
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append(tinfo)

    async def new(self, name: str, time: int, message: Message) -> TimerInfo:
        await bot.loop_wrapper.create_task(self.timer(name, time, message))
        return TimerInfo(name, datetime.datetime.now() + datetime.timedelta(seconds=time))

    async def timer(self, name: str, time: int, message: Message) -> None:
        await asyncio.sleep(time)
        await message.reply(f"{name}'s are ready! Switch off the oven quickly")
        self.storage[message.from_user.id].pop(0)


db = DummyDB()


@bot.on.message(Markup(["/ravioli", "/ravioli <ravioli_name>"]))
async def start(message: Message, ravioli_name: str = "Ravioli") -> str:
    ravioli = await db.new(ravioli_name, RAVIOLI_TIME_TO_COOK, message)
    db.add(message.from_user.id, ravioli)
    return f"Timer for ravioli {ravioli_name!r} is set!"


@bot.on.message(Text("/cooking"))
async def cooking(message: Message):
    boiling = db.get(message.from_user.id)
    if not boiling:
        await message.answer("Nothing is cooking right now!")
        return
    text = "\n".join(
        "{}. {} will be ready at {}".format(
            index,
            record.name,
            record.end_time.strftime("%m.%d.%Y %H:%M"),
        )
        for index, record in enumerate(boiling, start=1)
    )
    await message.answer("Boiling raviolies:\n\n" + text)


bot.run_forever(skip_updates=True)
