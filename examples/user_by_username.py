"""
The example uses the aiosqlite driver. It is recommended to use asynchronous drivers
to work with databases.
"""

import aiosqlite  # type: ignore
from fntypes.co import Nothing, Some, Option

from telegrinder import ABCMiddleware, API, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.model import decoder
from telegrinder.modules import logger
from telegrinder.rules import Markup, MessageEntities
from telegrinder.types import User
from telegrinder.types.enums import MessageEntityType

db_path = "examples/assets/users.db"
bot = Telegrinder(API(Token.from_env()))
logger.set_level("INFO")


async def create_table():
    async with aiosqlite.connect(db_path) as conn:
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
        resulting_row[column_name] = (
            bool(value)
            if column_name in (as_bool or ())
            and value in (0, 1)
            else value
        )
    return resulting_row


class DummyDatabase:
    def user_data(self, user: User) -> dict:
        return {
            k: (v.unwrap() if v else None)
            if isinstance(v, Some | type(Nothing))
            else v
            for k, v in user.to_dict(
                exclude_fields={
                    "supports_inline_queries",
                    "added_to_attachment_menu",
                    "can_read_all_group_messages",
                    "can_join_groups",
                }
            ).items()
        }

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
                    """, self.user_data(user)
                )
            await conn.commit()
    
    async def get_user(self, username: str) -> Option[User]:
        async with (
            aiosqlite.connect(db_path) as conn,
            conn.cursor() as cur,
        ):
            row = await (
                await cur.execute(
                    "SELECT * FROM users WHERE username = ?",
                    (username,)
                )
            ).fetchone()
            if row is None:
                return Nothing()
            return decoder.convert(
                obj=get_result_with_names(cur, row, as_bool={"is_premium", "is_bot"}),
                type=Option[User],
            )


db = DummyDatabase()


@bot.on.message.register_middleware()
class UserRegistrarMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if event.from_ and event.from_user.username:
            await db.set_user(event.from_user)
        return True


@bot.on.message(
    MessageEntities(MessageEntityType.MENTION)
    & Markup("/get_user @<username>")
)
async def get_user(message: Message, username: str):
    match await db.get_user(username):
        case Some(user):
            await message.reply(
                f"""
                id -> {user.id}
                is bot -> {'yes' if user.is_bot else 'no'}
                first name -> {user.first_name} 
                last name -> {user.last_name.unwrap_or('')}
                is premium -> {'yes' if user.is_premium.unwrap_or(False) else 'no'}
                lang code -> {user.language_code.unwrap()}
                """
                .replace("    ", "")
            )
        case Nothing():
            await message.reply(f"User with username {username!r} not found!")


bot.loop_wrapper.on_startup.append(create_table())
bot.run_forever()
