import typing

import aiosqlite  # type: ignore

from telegrinder.modules import logger
from telegrinder.node import per_call, scalar_node


@per_call  # type: ignore
@scalar_node
class DB:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:  # type: ignore
        connection = await aiosqlite.connect("test.db")  # type: ignore
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()  # type: ignore


async def create_tables() -> None:
    async with aiosqlite.connect("test.db") as conn:  # type: ignore
        await conn.execute(  # type: ignore
            "create table if not exists admins(id integer primary key autoincrement, telegram_id text unique)"
        )
