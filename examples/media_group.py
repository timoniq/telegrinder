"""Example of handling media groups with MediaGroupView.

This example demonstrates how to use the MediaGroupView to handle
media groups sent by users. Media groups are collections
of photos, videos or other media sent together.
"""

import logging

from telegrinder import API, Telegrinder, Token
from telegrinder.node import Caption, MediaGroup

# Set up logging
logging.basicConfig(level=logging.INFO)

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.media_group()
async def handle_media_group(
    media_group: MediaGroup, caption: Caption | None = None
):  # #287 fntypes.Option[Caption]
    """Handle media groups (albums)."""
    media_count = len(media_group.items)

    # Get media types in the group
    media_types = []
    for msg in media_group.items:
        if msg.photo.unwrap_or(None):
            media_types.append("photo")
        elif msg.video.unwrap_or(None):
            media_types.append("video")
        elif msg.document.unwrap_or(None):
            media_types.append("document")
        elif msg.audio.unwrap_or(None):
            media_types.append("audio")
        elif msg.animation.unwrap_or(None):
            media_types.append("animation")

    # Create response message
    media_list = ", ".join(set(media_types))
    response = (
        f"📁 Received media group with {media_count} items!\n"
        f"🏷️ Media types: {media_list}\n"
        f"📝 Caption: {caption or 'no caption'}"  # #287 caption.unwrap_or('no caption')
    )

    return response


bot.run_forever()
