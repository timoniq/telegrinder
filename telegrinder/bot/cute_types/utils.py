import collections
import typing

from telegrinder.tools.formatting.html_formatter import HTMLFormatter, StringFormatter, link, pre_code, tg_emoji
from telegrinder.tools.strings import to_utf16_map, utf16_to_py_index
from telegrinder.types.enums import ContentType, MessageEntityType
from telegrinder.types.methods_utils import get_params
from telegrinder.types.objects import (
    InputFile,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    MessageEntity,
    ReactionEmoji,
    ReactionType,
    ReactionTypeEmoji,
)

type InputMedia = typing.Union[
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
]

type MediaType = typing.Literal["animation", "audio", "document", "photo", "video"]

EntitiesDict = collections.defaultdict[int, list[MessageEntity]]

MEDIA_TYPES: typing.Final[tuple[ContentType, ...]] = (
    ContentType.ANIMATION,
    ContentType.AUDIO,
    ContentType.DOCUMENT,
    ContentType.PHOTO,
    ContentType.VIDEO,
)
INPUT_TYPES: typing.Final[tuple[type[InputMedia], ...]] = (
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)
INPUT_MEDIA_TYPES: typing.Final[dict[ContentType, type[InputMedia]]] = dict(zip(MEDIA_TYPES, INPUT_TYPES))
HTML_FORMAT_ENTITIES: typing.Final[tuple[MessageEntityType, ...]] = (
    MessageEntityType.PRE,
    MessageEntityType.CODE,
    MessageEntityType.TEXT_LINK,
    MessageEntityType.CUSTOM_EMOJI,
    *tuple(x for x in MessageEntityType if x.name.lower() in StringFormatter.__formatters__),
)


def build_html(text: str, entities: list[MessageEntity], /) -> str:
    utf16_map = to_utf16_map(text)
    text_length_utf16 = utf16_map[-1]
    events = set[int]()

    for entity in entities:
        events.add(entity.offset)
        events.add(entity.offset + entity.length)

    events = sorted(events)
    utf16_to_py = {u: utf16_to_py_index(utf16_map, u) for u in events + [0, text_length_utf16]}

    opens = EntitiesDict(list)
    closes = EntitiesDict(list)

    for entity in entities:
        opens[entity.offset].append(entity)
        closes[entity.offset + entity.length].append(entity)

    result = list[str]()
    stack = collections.deque[MessageEntity]()
    utf16_pos = 0

    while utf16_pos < text_length_utf16:
        py_start = utf16_to_py[utf16_pos]
        next_events = [u for u in events if u > utf16_pos]
        next_utf16 = min(next_events) if next_events else text_length_utf16
        py_end = utf16_to_py[next_utf16]

        if closes[utf16_pos]:
            for _ in closes[utf16_pos]:
                stack.pop()

        if opens[utf16_pos]:
            for e in sorted(opens[utf16_pos], key=lambda e: e.length, reverse=True):
                stack.append(e)

        chunk = text[py_start:py_end]
        formatted = chunk

        for e in reversed(stack):
            if (formatter := StringFormatter.__formatters__.get(e.type.name.lower())) is not None:
                formatted = formatter(formatted)
            elif e.type in (MessageEntityType.PRE, MessageEntityType.CODE):
                formatted = pre_code(formatted, lang=e.language.unwrap_or_none())
            elif e.type == MessageEntityType.TEXT_LINK:
                formatted = link(e.url.unwrap(), text=formatted)
            elif e.type == MessageEntityType.CUSTOM_EMOJI:
                formatted = tg_emoji(formatted, emoji_id=e.custom_emoji_id.map(int).unwrap())

        result.append(formatted)
        utf16_pos = next_utf16

    return HTMLFormatter().join(result)


def compose_reactions(
    reactions: str | ReactionEmoji | ReactionType | list[str | ReactionEmoji | ReactionType],
    /,
) -> list[ReactionType]:
    if not isinstance(reactions, list):
        reactions = [reactions]
    return [
        (
            ReactionTypeEmoji(emoji)
            if isinstance(emoji, ReactionEmoji)
            else (ReactionTypeEmoji(ReactionEmoji(emoji)) if isinstance(emoji, str) else emoji)
        )
        for emoji in reactions
    ]


def input_media(
    type: MediaType,
    media: str | InputFile,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    **other: typing.Any,
) -> InputMedia:
    return INPUT_MEDIA_TYPES[ContentType(type)](**get_params(locals()))


__all__ = ("build_html", "compose_reactions", "input_media")
