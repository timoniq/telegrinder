import aiosqlite  # type: ignore

from examples.composition import DB
from telegrinder import API, Message, Telegrinder, Token, node
from telegrinder.bot.rules import ABCRule, Markup
from telegrinder.modules import logger

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


class IsChat(ABCRule):
    async def check(self, source: node.Source) -> bool:
        return source.chat.id < 0


@bot.on.message(IsChat())
async def mention_by_user_handler(message: Message, p: node.Photo):
    photo_size = p.sizes[-1]
    await message.answer("Nice photo {}".format(photo_size.height / photo_size.width))


@bot.on.message(Markup("/vibe <vibe_name>"))
async def vibe_handler(m: Message, db: DB, vibe_name: str):
    counter = await (
        await db.execute("select counter from vibes where name = ? limit 1", (vibe_name,))
    ).fetchone()
    if not counter:
        await db.execute("insert into vibes(name, counter) values (?, ?)", (vibe_name, 0))
        await db.commit()
        counter = 1
    else:
        counter = counter[0] + 1

    await db.execute("update vibes set counter = ? where name = ?", (counter, vibe_name))
    await db.commit()

    await m.answer(f"VIBE {vibe_name} counter: {counter}")


@bot.loop_wrapper.lifespan.on_startup
async def create_tables() -> None:
    async with aiosqlite.connect("test.db") as conn:
        await conn.execute(
            "create table if not exists vibes("
            "id integer primary key autoincrement, "
            "name text, "
            "counter int32"
            ")"
        )


bot.run_forever()
