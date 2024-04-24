"""
The example uses the aiosqlite driver. It is recommended to use asynchronous drivers
to work with databases.
"""

import typing

import aiosqlite  # type: ignore
from fntypes.co import Nothing, Some

from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.model import decoder
from telegrinder.modules import logger
from telegrinder.msgspec_utils import Option
from telegrinder.rules import Markup, MessageEntities
from telegrinder.types import User
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity

db_path = "examples/assets/users.db"
bot = Telegrinder(API(Token.from_env()))
logger.set_level("DEBUG")


async def create_table():
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
        resulting_row[column_name] = (
            bool(value)
            if column_name in (as_bool or ())
            and value in (0, 1)
            else value
        )
    return resulting_row


class DummyDatabase:
    @staticmethod
    def convert_user_to_dict(user: User) -> dict[str, typing.Any]:
        return {
            k: v
            if not isinstance(v, Some | Nothing)
            else v.unwrap_or_none()
            for k, v in user.to_dict().items()
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
                    """,
                    self.convert_user_to_dict(user),
                )
            await conn.commit()
    
    async def get_user_by_username(self, username: str) -> Option[User]:
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
    
    async def get_user_by_id(self, user_id: int) -> Option[User]:
        async with (
            aiosqlite.connect(db_path) as conn,
            conn.cursor() as cur,
        ):
            row = await (
                await cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
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
        if event.from_:
            await db.set_user(event.from_user)
        return True


@bot.on.message(
    Markup("/get_user <user_id:int>")
    | Markup("/get_user @<username>")
    | MessageEntities(MessageEntityType.TEXT_MENTION)
)
async def get_user(
    message: Message,
    message_entities: list[MessageEntity] | None = None,
    username: str | None = None,
    user_id: int | None = None
):
    if message_entities and message_entities[0].type == MessageEntityType.TEXT_MENTION:
        mentioned_user = message_entities[0].user.unwrap()
        user = await db.get_user_by_id(mentioned_user.id)
        if not user:
            await db.set_user(mentioned_user)
        user = Some(mentioned_user)
    elif username is not None:
        user = await db.get_user_by_username(username)
    else:
        assert user_id
        user = await db.get_user_by_id(user_id)

    match user:
        case Some(u):
            await message.reply(
                f"""
                id -> {u.id}
                is bot -> {'yes' if u.is_bot else 'no'}
                first name -> {u.first_name} 
                last name -> {u.last_name.unwrap_or('')}
                is premium -> {'yes' if u.is_premium.unwrap_or(False) else 'no'}
                lang code -> {u.language_code.unwrap()!r}
                """
                .replace("    ", "")
            )
        case Nothing():
            await message.reply(f"User with {'username' if username else 'id'} {username or user_id!r} not found!")


bot.loop_wrapper.on_startup.append(create_table())
bot.run_forever()
