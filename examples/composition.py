import logging
import typing

import aiosqlite

from telegrinder import API, Telegrinder, Token
from telegrinder.bot.dispatch import CompositionDispatch
from telegrinder.node import Photo, ScalarNode, Source, Text, generate

api = API(token=Token.from_env())
bot = Telegrinder(api, dispatch=CompositionDispatch())
logging.basicConfig(level=logging.INFO)


async def create_tables():
    async with aiosqlite.connect("test.db") as conn:
        await conn.execute(
            "create table if not exists logs("
            "id integer primary key autoincrement, "
            "msg text"
            ")"
        )


class DB(ScalarNode, aiosqlite.Connection):
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        yield connection
        logging.info("Closing connection")
        await connection.close()


@bot.on()
async def photo_handler(photo: Photo, source: Source, db: DB):
    await source.send(
        "File ID: " + photo.sizes[-1].file_id,
    )
    await db.execute("insert into logs(msg) values (?)", (photo.sizes[-1].file_id,))
    await db.commit()
    logging.info("Finished handling")


# Container generated node examples

@bot.on(container=[
    generate((Text,), lambda text: text == "hello"),
    generate((Source,), lambda src: src.chat.username.unwrap_or_none() == "weirdlashes"),
])
async def hi_handler(source: Source):
    await source.send("Hi !!")


@bot.on(container=[
    generate((Text,), lambda text: int(text) if text.isdigit() else None)
])
async def integer_handler(
    source: Source,
    container: tuple[int],
):
    integer, = container
    await source.send("{} + 3 = {}".format(integer, integer + 3))


bot.loop_wrapper.add_task(create_tables())
bot.run_forever()
