import typing

import aiosqlite  # type: ignore

from telegrinder.modules import logger
from telegrinder.node import PER_EVENT, ScalarNode


# Pure node examples
class DB(ScalarNode, aiosqlite.Connection):
    # DB connection will be only opened once per event
    scope = PER_EVENT

    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()
