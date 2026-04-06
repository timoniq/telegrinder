import collections
import typing

from telegrinder.tools.formatting.html import FORMATTERS, date_time, link, pre_code, tg_emoji
from telegrinder.tools.strings import to_utf16_map, utf8_utf16_length, utf16_to_py_index
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

MEDIA_TYPES: typing.Final = (
    ContentType.ANIMATION,
    ContentType.AUDIO,
    ContentType.DOCUMENT,
    ContentType.PHOTO,
    ContentType.VIDEO,
)
INPUT_TYPES: typing.Final = (
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)
INPUT_MEDIA_TYPES: typing.Final[dict[ContentType, type[InputMedia]]] = dict(zip(MEDIA_TYPES, INPUT_TYPES))


def build_html(text: str, entities: list[MessageEntity], /) -> str:
    if not text or not entities:
        return ""

    utf8_text_utf16_length = utf8_utf16_length(text)
    events = set[int]()

    for entity in entities:
        events.add(entity.offset)
        events.add(entity.offset + entity.length)

    events = sorted(events)
    utf16_map = to_utf16_map(text)
    utf16_index_map = {u: utf16_to_py_index(utf16_map, u) for u in events + [0, utf8_text_utf16_length]}

    opens = EntitiesDict(list)
    closes = EntitiesDict(list)

    for entity in entities:
        opens[entity.offset].append(entity)
        closes[entity.offset + entity.length].append(entity)

    result = list[str]()
    stack = collections.deque[MessageEntity]()
    utf16_pos = 0

    while utf16_pos < utf8_text_utf16_length:
        start_index = utf16_index_map[utf16_pos]
        next_events = tuple(u for u in events if u > utf16_pos)
        next_utf16_pos = min(next_events) if next_events else utf8_text_utf16_length
        end_index = utf16_index_map[next_utf16_pos]

        for _ in closes.get(utf16_pos, ()):
            stack.pop()

        for e in sorted(opens.get(utf16_pos, ()), key=lambda e: e.length, reverse=True):
            stack.append(e)

        formatted = text[start_index:end_index]

        for e in reversed(stack):
            if (formatter := FORMATTERS.get(e.type.value)) is not None:
                formatted = formatter(formatted)
            elif e.type in (MessageEntityType.PRE, MessageEntityType.CODE):
                formatted = pre_code(formatted, lang=e.language.unwrap_or_none())
            elif e.type == MessageEntityType.TEXT_LINK:
                formatted = link(e.url.expect("URL for text link is required."), text=formatted)
            elif e.type == MessageEntityType.CUSTOM_EMOJI:
                formatted = tg_emoji(formatted, emoji_id=e.custom_emoji_id.expect("Custom emoji id is required."))
            elif e.type == MessageEntityType.DATETIME:
                formatted = date_time(
                    formatted,
                    e.unix_time.expect("Unix timestamp is required."),
                    format=e.date_time_format.unwrap_or_none(),
                )

        result.append(formatted)
        utf16_pos = next_utf16_pos

    return "".join(result)


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
