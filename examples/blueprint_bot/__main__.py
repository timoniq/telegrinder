from .client import bot, dp

dp.load_from_dir("handlers")
bot.run_forever()
