from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.modules import logger

from . import admin, start, with_enum

dp = Dispatch()
logger.set_level("INFO")

for blueprint in (admin, start, with_enum):
    dp.load(blueprint.dp)

bot = Telegrinder(API(Token.from_env()), dispatch=dp)
bot.run_forever()
