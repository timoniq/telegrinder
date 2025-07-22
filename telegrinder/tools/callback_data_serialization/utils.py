from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.callback_data_serialization.abc import ABCDataSerializer

IDENT_KEY: typing.Final[str] = "__key__"
SERIALIZER_KEY: typing.Final[str] = "__serializer__"


def get_model_ident_key(model: typing.Any, /) -> str | None:
    return getattr(model, IDENT_KEY, None)


def get_model_serializer(model: typing.Any, /) -> type[ABCDataSerializer[typing.Any]] | None:
    return getattr(model, SERIALIZER_KEY, None)


__all__ = ("get_model_ident_key", "get_model_serializer")
