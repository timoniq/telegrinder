from telegrinder.modules import logger

from .client import bot, dp

logger.set_level("INFO")
dp.load_from_dir("handlers")
bot.run_forever()
