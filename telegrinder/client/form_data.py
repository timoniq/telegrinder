import typing

from telegrinder.msgspec_utils import encoder


def encode_form_data(
    data: dict[str, typing.Any],
    files: dict[str, tuple[str, typing.Any]],
    /,
) -> dict[str, str]:
    context = dict(files=files)
    return {
        k: encoder.encode(v, context=context).strip('"')  # Remove quoted string
        if not isinstance(v, str)
        else v
        for k, v in data.items()
    }


class MultipartFormProto(typing.Protocol):
    def add_field(
        self,
        name: str,
        value: typing.Any,
        /,
        *,
        filename: str | None = None,
    ) -> None: ...


__all__ = ("MultipartFormProto", "encode_form_data")
