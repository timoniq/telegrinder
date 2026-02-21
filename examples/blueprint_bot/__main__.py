from .client import bot, dp

dp.load_from_dir("blueprint_bot/handlers")
bot.run_forever(skip_updates=True)
