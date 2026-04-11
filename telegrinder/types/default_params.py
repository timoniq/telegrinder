from __future__ import annotations

import typing

from telegrinder.types.methods_utils import ProxiedDict

if typing.TYPE_CHECKING:
    from telegrinder.types.objects import *  # noqa: F403


class DefaultParameters(typing.TypedDict):
    parse_mode: str
    text_parse_mode: str
    allow_paid_broadcast: bool
    link_preview_options: LinkPreviewOptions
    disable_notification: bool
    protect_content: bool


DEFAULT_PARAMETERS: typing.Final = ProxiedDict(DefaultParameters)


__all__ = ("DEFAULT_PARAMETERS", "DefaultParameters")
