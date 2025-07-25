"""Example of handling media groups with MediaGroupView.

This example demonstrates how to use the MediaGroupView to handle
media groups sent by users. Media groups are collections
of photos, videos or other media sent together.
"""

from fntypes.library.monad.option import Option

from telegrinder import API, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.node import Caption, MediaGroup

logger.set_level("INFO")
api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.media_group()
async def handle_media_group(media_group: MediaGroup, caption: Option[Caption]) -> str:
    return (
        f"📁 Received media group with {len(media_group.items)} items!\n"
        f"🏷️ Media types: {', '.join(set(message.content_type.value for message in media_group.items))}\n"
        f"📝 Caption: {caption.unwrap_or('no caption')}"
    )


bot.run_forever()
