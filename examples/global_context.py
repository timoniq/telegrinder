import typing
from functools import reduce

from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.modules import logger
from telegrinder.rules import Markup, MessageEntities, Text
from telegrinder.tools.formatting import HTMLFormatter, bold, code_inline
from telegrinder.tools.formatting.html import TagFormat
from telegrinder.tools.global_context import GlobalContext, ctx_var
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import User

logger.set_level("INFO")
api = API(token=Token.from_env())
bot = Telegrinder(api)


class ImportantContext(GlobalContext):
    __ctx_name__ = "important_ctx"

    formatting: bool = False
    users: typing.ClassVar[dict[str, User]] = ctx_var({}, const=True)


global_ctx = ImportantContext()


def formatting_text(*fmt_texts: str | TagFormat) -> dict:
    params = {"text": "", "parse_mode": None}
    if not global_ctx.formatting:
        params["text"] = "".join(map(str, fmt_texts))
        return params
    params["parse_mode"] = HTMLFormatter.PARSE_MODE
    params["text"] = HTMLFormatter("".join(reduce(lambda x, y: x + y, fmt_texts)))
    return params


class UserRegistrarMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if event.from_ and event.from_user.username:
            # register user by username
            global_ctx.users.setdefault(
                event.from_user.username.unwrap(), event.from_user
            )
        return True


@bot.on.message(Text("/formatting"))
async def formatting(message: Message):
    global_ctx.formatting = not global_ctx.formatting
    await message.answer(
        **formatting_text(
            "Formatting ",
            bold("enabled!" if global_ctx.formatting else "disabled!"),
        )
    )


@bot.on.message(
    MessageEntities([MessageEntityType.MENTION, MessageEntityType.URL])
    & Markup(["/get_user @<username>", "/get_user t.me/<username>"])
)
async def get_user_by_username(message: Message, username: str):
    user = global_ctx.users.get(username)
    if user is None:
        await message.answer(
            **formatting_text("User with username ", bold(username), " not found!")
        )
        return
    await message.answer(**formatting_text("User: ", code_inline(repr(user))))


bot.on.message.middlewares.append(UserRegistrarMiddleware())
bot.run_forever()
