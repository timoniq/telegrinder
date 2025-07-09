import typing

from telegrinder.types.enums import ContentType
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


__all__ = ("compose_reactions", "input_media")
