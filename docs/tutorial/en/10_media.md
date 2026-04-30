# Media

Bots almost never work with text only. In telegrinder media work usually falls into three common scenarios:

- sending files
- downloading files
- handling media groups

## Sending a file

A simple way to send a local file is to build an `InputFile`:

```python
import pathlib

from telegrinder import Message
from telegrinder.types import InputFile

cool_bytes = pathlib.Path("examples/assets/satie.jpeg").read_bytes()


@bot.on.message(Text("/photo"))
async def start(message: Message) -> None:
    await message.answer_photo(
        InputFile("satie.jpeg", cool_bytes),
        caption="Erik",
    )
```

This works well when the file already exists on disk or in memory.

---

## Resolving and downloading a file

If a user sends a photo, you can get its `file_id`, resolve the Telegram file path, and then download the bytes.

```python
import pathlib

from telegrinder import Message
from telegrinder.rules import ABCRule

photos_path = pathlib.Path("photos")
photos_path.mkdir(exist_ok=True)


class HasPhoto(ABCRule):
    async def check(self, message: Message) -> bool:
        return bool(message.photo.unwrap_or_none())


@bot.on.message(HasPhoto())
async def downloader(message: Message) -> str:
    photo_file = (await message.api.get_file(file_id=message.photo.unwrap()[-1].file_id)).unwrap()
    photo_path = photo_file.file_path.unwrap()

    path = photos_path / pathlib.Path(photo_path.split("/")[-1])
    path.write_bytes((await message.api.download_file(photo_path)).unwrap())
    return "Photo downloaded!"
```

---

## Attachment nodes

You do not always need to unpack media manually. Telegrinder already provides useful built-in nodes:

- `Attachment`
- `Photo`
- `Video`
- `Document`
- `Audio`
- `Voice`
- `Caption`
- `File[...]`

For example:

```python
from telegrinder import Message, node
from telegrinder.node import File, Photo


@bot.on.message()
async def photo_handler(message: Message, file: File[Photo]) -> None:
    await message.answer(f"File path: {file.file_path.unwrap_or('None')}")
```

That is much nicer than repeating attachment extraction logic in every handler.

---

## Media groups

Media groups are a separate case because Telegram sends multiple media items as one set.

For that there is a dedicated `media_group` view and a `MediaGroup` node:

```python
from kungfu.library.monad.option import Option

from telegrinder.node import Caption, MediaGroup


@bot.on.media_group()
async def handle_media_group(media_group: MediaGroup, caption: Option[Caption]) -> str:
    return (
        f"Received media group with {len(media_group.items)} items\n"
        f"Caption: {caption.unwrap_or('no caption')}"
    )
```

That is much better than manually merging updates by `media_group_id`.

---

## Useful references

- [examples/upload.py](https://github.com/timoniq/telegrinder/blob/dev/examples/upload.py)
- [examples/download_photo.py](https://github.com/timoniq/telegrinder/blob/dev/examples/download_photo.py)
- [examples/media_group.py](https://github.com/timoniq/telegrinder/blob/dev/examples/media_group.py)
- [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py)

[>> Next: Handling errors](11_handling_errors.md)
