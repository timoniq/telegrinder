import typing

from telegrinder.model import get_params
from telegrinder.types.objects import (
    InputFile,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    LinkPreviewOptions,
    MessageEntity,
    ReactionEmoji,
    ReactionType,
    ReactionTypeEmoji,
    ReplyParameters,
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
            ReactionTypeEmoji("emoji", emoji)
            if isinstance(emoji, ReactionEmoji)
            else (ReactionTypeEmoji("emoji", ReactionEmoji(emoji)) if isinstance(emoji, str) else emoji)
        )
        for emoji in ([reactions] if isinstance(reactions, str) else reactions)  # type: ignore
    ]


def compose_reply_params(
    message_id: int | None,
    chat_id: int | str | None,
    *,
    allow_sending_without_reply: bool | None = None,
    quote: str | None = None,
    quote_parse_mode: str | None = None,
    quote_entities: list[MessageEntity] | None = None,
    quote_position: int | None = None,
    **other: typing.Any,
) -> ReplyParameters:
    return ReplyParameters(**get_params(locals()))


def compose_link_preview_options(
    *,
    is_disabled: bool | None = None,
    url: str | None = None,
    prefer_small_media: bool | None = None,
    prefer_large_media: bool | None = None,
    show_above_text: bool | None = None,
    **other: typing.Any,
) -> LinkPreviewOptions:
    return LinkPreviewOptions(**get_params(locals()))


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


__all__ = (
    "compose_link_preview_options",
    "compose_reactions",
    "compose_reply_params",
    "input_media",
)
