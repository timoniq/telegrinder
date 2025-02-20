import pathlib

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.dispatch.context import Context
from telegrinder.rules import MessageRule

bot = Telegrinder(API(Token.from_env()))
photos_path = pathlib.Path("photos")
photos_path.mkdir(exist_ok=True)


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.photo.unwrap_or_none())


@bot.on.message(HasPhoto())
async def downloader(message: Message) -> str:
    photo_file = (await message.ctx_api.get_file(file_id=message.photo.unwrap()[-1].file_id)).unwrap()
    photo_path = photo_file.file_path.unwrap()

    path = photos_path / pathlib.Path(photo_path.split("/")[-1])
    path.write_bytes(
        await message.ctx_api.download_file(photo_path),
    )
    return "Photo downloaded!"


bot.run_forever()
