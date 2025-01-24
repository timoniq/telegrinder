import typing

import aiosqlite  # type: ignore

from telegrinder.modules import logger
from telegrinder.node import ScalarNode, per_call


class DB(ScalarNode, aiosqlite.Connection):
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()


# DB connection will be only opened once per event
# to change this and resolve node each time when needed use:
@per_call
class DB2(ScalarNode, aiosqlite.Connection): ...


async def create_tables() -> None:
    async with aiosqlite.connect("test.db") as conn:
        await conn.execute(
            "create table if not exists admins(id integer primary key autoincrement, telegram_id text unique)"
        )
