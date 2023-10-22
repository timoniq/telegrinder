from . import admin, start, with_enum
from telegrinder import Dispatch, Telegrinder, API, Token

dp = Dispatch()

for blueprint in (admin, start, with_enum):
    dp.load(blueprint.dp)


bot = Telegrinder(API(Token.from_env()), dispatch=dp)
bot.run_forever()
