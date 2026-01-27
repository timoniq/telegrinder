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
        else v.__str__()
        for k, v in data.items()
    }


@typing.runtime_checkable
class MultipartBuilderProto(typing.Protocol):
    def add_field(
        self,
        name: str,
        value: typing.Any,
        /,
        filename: str | None = None,
        **kwargs: typing.Any,
    ) -> None: ...

    def build(self) -> typing.Any: ...


__all__ = ("MultipartBuilderProto", "encode_form_data")
