import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Argument, Command

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


def character(c: str) -> str | None:
    if len(c) != 1:
        return None
    return c


def sentence(s: str) -> str | None:
    if not s.startswith("'") and s.endswith("'"):
        return None
    s = s.removeprefix("'").removesuffix("'")
    return s


def int_validator(s: str) -> int | None:
    if not s.isdigit():
        return None
    return int(s)


# Try:
# /split 'hello,_my_friend' _ 1
# /split 'hello,_my_friend' _
# /split 'hello, my friend'   2
# /split 'hello, my friend' ,


@bot.on.message(
    Command(
        "split",
        Argument("string", [sentence]),
        Argument("sep", [character], optional=True),
        Argument("count", [int_validator], optional=True),
    )
)
async def split_handler(
    message: Message, string: str, sep: str = " ", count: int | None = None
) -> None:
    await message.answer(
        " | ".join(string.split(sep, count) if count is not None else string.split(sep))
    )


bot.run_forever()
