import logging
import typing
import aiosqlite

from telegrinder import API, Telegrinder, Token

from telegrinder.bot.dispatch import CompositionDispatch
from telegrinder.node import Photo, Source, ScalarNode

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


bot.loop_wrapper.add_task(create_tables())
bot.run_forever()
