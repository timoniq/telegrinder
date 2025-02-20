import typing

import aiosqlite  # type: ignore

from telegrinder.modules import logger
from telegrinder.node import NodeScope, scalar_node


@scalar_node(scope=NodeScope.PER_CALL)
class DB:
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()


async def create_tables() -> None:
    async with aiosqlite.connect("test.db") as conn:
        await conn.execute(
            "create table if not exists admins(id integer primary key autoincrement, telegram_id text unique)"
        )
