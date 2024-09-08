from telegrinder.modules import logger

from . import admin, start, with_enum
from .client import bot, dp

logger.set_level("INFO")

for blueprint in (admin, start, with_enum):
    dp.load(blueprint.dp)


bot.run_forever()
