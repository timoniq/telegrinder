import typing

import aiosqlite  # type: ignore

from telegrinder import API, Telegrinder, Token
from telegrinder.bot import rules
from telegrinder.bot.dispatch import CompositionDispatch
from telegrinder.modules import logger
from telegrinder.node import Photo, RuleContext, ScalarNode, Source, Text, generate

api = API(token=Token.from_env())
bot = Telegrinder(api, dispatch=CompositionDispatch())
logger.set_level("INFO")


@bot.loop_wrapper.lifespan.on_startup
async def create_tables() -> None:
    async with aiosqlite.connect("test.db") as conn:
        await conn.execute(
            "create table if not exists logs("
            "id integer primary key autoincrement, "
            "msg text"
            ")"
        )


# Pure node examples
class DB(ScalarNode, aiosqlite.Connection):
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        yield connection
        logger.info("Closing connection")
        await connection.close()


@bot.on()
async def photo_handler(photo: Photo, source: Source, db: DB):
    await source.send("File ID: " + photo.sizes[-1].file_id)
    await db.execute("insert into logs(msg) values (?)", (photo.sizes[-1].file_id,))
    await db.commit()
    logger.info("Finished handling")


# Container generated node examples
@bot.on(
    generate((Text,), lambda text: text == "hello"),
    generate((Source,), lambda src: src.chat.username.unwrap_or_none() == "weirdlashes"),
)
async def hi_handler(source: Source):
    await source.send("Hi !!")


@bot.on(generate((Text,), lambda text: int(text) if text.isdigit() else None))
async def integer_handler(source: Source, container: tuple[int]):
    (integer,) = container
    await source.send("{} + 3 = {}".format(integer, integer + 3))


# Rule node examples
@bot.on()
async def handler_ruleset_as_context(
    ctx: RuleContext[rules.Markup("/name <name>"),],
    src: Source,
) -> None:
    name = ctx["name"]
    await src.send(f"Hi, {name}")


class Context(
    RuleContext[
        rules.Markup("<a:int> / <b:int> = <c:float>"),
        rules.IsUser(),
    ]
):
    a: int
    b: int
    c: float


@bot.on()
async def handler_ruleset_dataclass_context(
    ctx: Context,
    src: Source,
) -> None:
    if ctx.a / ctx.b == ctx.c:
        await src.send("Right! ^___^")
    else:
        await src.send("Wrong! >:(")


bot.run_forever()
