import typing
from functools import reduce

from telegrinder import API, ABCMiddleware, Message, Telegrinder, Token
from telegrinder.bot import Context
from telegrinder.modules import logger
from telegrinder.rules import Markup, MessageEntities, Text
from telegrinder.tools.formatting.html_formatter import HTMLFormatter, bold, code_inline
from telegrinder.tools.global_context import GlobalContext, ctx_var
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity, User

logger.set_level("INFO")
api = API(token=Token.from_env())
bot = Telegrinder(api)


class ImportantContext(GlobalContext):
    __ctx_name__ = "important_ctx"

    formatting: bool = False
    users: dict[int, User] = ctx_var(default={}, const=True)


global_ctx = ImportantContext()


def formatting_text(*fmt_texts: str) -> dict[str, typing.Any]:
    params = {"text": "", "parse_mode": None}
    if not global_ctx.formatting:
        params["text"] = "".join(map(str, fmt_texts))
        return params
    params["parse_mode"] = HTMLFormatter.PARSE_MODE
    params["text"] = HTMLFormatter("".join(reduce(lambda x, y: x + y, fmt_texts)))
    return params


@bot.dispatch.message.register_middleware()
class UserRegistrarMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        if event.from_:
            global_ctx.users[event.from_user.id] = event.from_user
        return True


@bot.on.message(Text("/formatting"))
async def formatting(_: Message) -> dict[str, typing.Any]:
    global_ctx.formatting = not global_ctx.formatting
    return formatting_text("Formatting ", bold("enabled!" if global_ctx.formatting else "disabled!"))


@bot.on.message(
    MessageEntities([MessageEntityType.TEXT_MENTION, MessageEntityType.MENTION, MessageEntityType.URL])
    & Markup(["/get_user @<username>", "/get_user t.me/<username>", "/get_user <username>"])
)
async def get_user_by_username(
    _: Message, username: str, message_entities: list[MessageEntity]
) -> dict[str, typing.Any]:
    if message_entities[0].type == MessageEntityType.TEXT_MENTION:
        user = message_entities[0].user.unwrap()
        global_ctx.users[user.id] = user
    else:
        user = None
        for u in global_ctx.users.values():
            if u.username.unwrap_or_none() == username:
                user = u

    if user is None:
        return formatting_text("User with username ", bold(username), " not found!")
    return formatting_text("User: ", code_inline(repr(user)))


bot.run_forever()
