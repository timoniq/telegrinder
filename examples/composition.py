import logging

from telegrinder import API, Telegrinder, Token

from telegrinder.bot.dispatch import CompositionDispatch
from telegrinder.node import Photo, Source

api = API(token=Token.from_env())
bot = Telegrinder(api, dispatch=CompositionDispatch())
logging.basicConfig(level=logging.INFO)

@bot.on()
async def photo_handler(photo: Photo, source: Source):
    await source.send(
        "File ID: " + photo.sizes[-1].file_id,
    )

bot.run_forever()
