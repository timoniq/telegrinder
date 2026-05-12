# Медиа

Бот почти всегда работает не только с текстом. В telegrinder с медиа обычно встречаются три сценария:

- отправить файл
- скачать файл
- обработать медиа-группу

## Отправка файла

Простой способ отправить локальный файл — собрать `InputFile`:

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

Такой способ хорош, когда файл уже у вас на диске или вы собрали его в памяти.

---

## Получение и скачивание файла

Если пользователь отправил фотографию, можно получить `file_id`, запросить путь через Telegram API и затем скачать байты.

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

## Ноды для вложений

Во многих случаях вручную разбирать сообщение не нужно. Для этого уже есть built-in ноды:

- `Attachment`
- `Photo`
- `Video`
- `Document`
- `Audio`
- `Voice`
- `Caption`
- `File[...]`

Например:

```python
from telegrinder import Message, node
from telegrinder.node import File, Photo


@bot.on.message()
async def photo_handler(message: Message, file: File[Photo]) -> None:
    await message.answer(f"Путь к файлу: {file.file_path.unwrap_or('None')}")
```

Это намного приятнее, чем повторять одну и ту же логику извлечения вложения в каждом хендлере.

---

## Медиа-группы

Отдельный случай это media groups, когда Telegram присылает несколько вложений как один набор.

Для этого есть специальный view `media_group` и нода `MediaGroup`:

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

Это удобнее, чем самостоятельно склеивать сообщения по `media_group_id`.

---

## Что посмотреть в примерах

- [examples/upload.py](https://github.com/timoniq/telegrinder/blob/dev/examples/upload.py)
- [examples/download_photo.py](https://github.com/timoniq/telegrinder/blob/dev/examples/download_photo.py)
- [examples/media_group.py](https://github.com/timoniq/telegrinder/blob/dev/examples/media_group.py)
- [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py)

[>> Next: Обработка ошибок](11_handling_errors.md)
