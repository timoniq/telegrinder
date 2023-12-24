import logging

from telegrinder import API, Telegrinder, Token

from telegrinder.bot.dispatch.view.composition import CompositionView
from telegrinder.node import Photo, Source

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

@bot.on.composition()
async def photo_handler(photo: Photo, source: Source):
    await source.send(f"File ID: {photo.sizes[-1].file_id}")

bot.run_forever()