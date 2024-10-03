import typing

from telegrinder.model import get_params
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

InputMedia: typing.TypeAlias = typing.Union[
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
]

INPUT_MEDIA_TYPES: typing.Final[dict[str, type[InputMedia]]] = {
    "animation": InputMediaAnimation,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
}


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
    type: typing.Literal["animation", "audio", "document", "photo", "video"],
    media: str | InputFile,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    **other: typing.Any,
) -> InputMedia:
    return INPUT_MEDIA_TYPES[type](**get_params(locals()))


__all__ = ("compose_reactions", "input_media")
