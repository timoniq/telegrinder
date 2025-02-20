"""The example uses the aiosqlite driver. It is recommended to use asynchronous drivers
to work with databases.
"""

import aiosqlite  # type: ignore
from fntypes.option import Nothing

from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.message import MessageRule
from telegrinder.model import decoder
from telegrinder.modules import logger
from telegrinder.msgspec_utils import Option
from telegrinder.rules import IsReply, Markup, MessageEntities, Text
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import User

db_path = "examples/assets/users.db"
bot = Telegrinder(API(Token.from_env()))
logger.set_level("INFO")


@bot.loop_wrapper.lifespan.on_startup
async def create_table() -> None:
    async with aiosqlite.connect(db_path) as conn:  # noqa: SIM117
        async with conn.cursor() as cur:
            await cur.execute(
                "create table if not exists users("
                "id integer unique,"
                "is_bot boolean,"
                "is_premium boolean,"
                "first_name varchar(64),"
                "last_name varchar(64),"
                "username varchar(32),"
                "language_code varchar(5))"
            )
            await conn.commit()


def get_result_with_names(
    cursor: aiosqlite.Cursor,
    row: aiosqlite.Row,
    as_bool: set[str] | None = None,
) -> dict:
    column_names = [d[0] for d in cursor.description]
    resulting_row = {}
    for index, column_name in enumerate(column_names):
        value = row[index]
        resulting_row[column_name] = bool(value) if column_name in (as_bool or ()) and value in (0, 1) else value
    return resulting_row


class DummyDatabase:
    async def set_user(self, user: User) -> None:
        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT OR REPLACE INTO users(
                        id, is_bot, first_name, last_name,
                        username, language_code, is_premium
                    ) VALUES (
                        :id, :is_bot, :first_name, :last_name,
                        :username, :language_code, :is_premium
                    );
                    """,
                    user.to_full_dict(),
                )
            await conn.commit()

    async def get_user_by_username(self, username: str) -> Option[User]:
        async with (
            aiosqlite.connect(db_path) as conn,
            conn.cursor() as cur,
        ):
            row = await (await cur.execute("SELECT * FROM users WHERE username = ?", (username,))).fetchone()
            if row is None:
                return Nothing()
            return decoder.convert(
                obj=get_result_with_names(cur, row, as_bool={"is_premium", "is_bot"}),
                type=Option[User],  # type: ignore
            )

    async def get_or_set_user(self, user: User) -> User:
        if (await self.get_user_by_id(user.id)).unwrap_or_none() is None:
            await self.set_user(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Option[User]:
        async with (
            aiosqlite.connect(db_path) as conn,
            conn.cursor() as cur,
        ):
            row = await (await cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))).fetchone()
            if row is None:
                return Nothing()
            return decoder.convert(
                obj=get_result_with_names(cur, row, as_bool={"is_premium", "is_bot"}),
                type=Option[User],  # type: ignore
            )


db = DummyDatabase()


@bot.on.message.register_middleware()
class UserRegistrarMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if event.from_:
            await db.set_user(event.from_user)
        if event.reply_to_message and event.reply_to_message.unwrap().from_:
            await db.set_user(event.reply_to_message.unwrap().from_user)
        return True


class MentionRule(
    MessageRule,
    requires=[
        Text("/get_user") & IsReply()
        | Markup("/get_user id<user_id:int>")
        | MessageEntities(MessageEntityType.TEXT_MENTION) & Markup("/get_user <!>")
        | MessageEntities(MessageEntityType.MENTION) & Markup("/get_user @<username>")
    ],
):
    async def check(self, message: Message, ctx: Context) -> bool:
        user = None

        match ctx:
            case {"message_entities": message_entities} if (
                message_entities[0].type == MessageEntityType.TEXT_MENTION
            ):
                user = await db.get_or_set_user(message_entities[0].user.unwrap())
            case {"username": username}:
                user = (await db.get_user_by_username(username)).unwrap_or_none()
            case {"user_id": user_id}:
                user = (await db.get_user_by_id(user_id)).unwrap_or_none()
            case _ if message.reply_to_message:
                user = message.reply_to_message.unwrap().from_.unwrap_or_none()

        if user is None:
            return False
        ctx.set("mentioned_user", user)
        return True


@bot.on.message(MentionRule())
async def get_user(_: Message, mentioned_user: User) -> str:
    return f"""
    Id -> {mentioned_user.id}
    Is bot -> {"✅" if mentioned_user.is_bot else "❌"}
    First name -> {mentioned_user.first_name}
    Last name -> {mentioned_user.last_name.unwrap_or(repr("UNKNOWN"))}
    Is premium -> {"✅" if mentioned_user.is_premium.unwrap_or(False) else "❌"}
    Language code -> {mentioned_user.language_code.unwrap_or(repr("UNKNOWN"))}
    """.replace("    ", "")


bot.run_forever()
