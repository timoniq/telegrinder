import typing

import vbml

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Markup
from telegrinder.tools.formatting import HTMLFormatter

api = API(token=Token.from_env())
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.dispatch.global_context.vbml_patcher.validator("operand")
class OperandValidator(vbml.ABCValidator):
    def check(self, value: str) -> str | None:
        return value if value in ("+", "-", "/", "*") else None


@bot.on.message(Markup(["/solve <a:int> <operand:operand> <b:int>"]))
async def solve(
    message: Message,
    a: int,
    b: int,
    operand: typing.Literal["+", "-", "/", "*"],
):
    statement = f"{a} {operand} {b}"
    await message.reply(
        HTMLFormatter("🧐 Result: {:bold+italic} = {:code_inline}").format(
            statement,
            eval(statement),
        ),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


@solve.error_handler(ZeroDivisionError)
async def zero_division_catcher() -> str:
    return "🧐 You can't divide by zero!!!"


bot.run_forever()
