import typing


def join_dicts[Key: typing.Hashable, Value](
    left_dict: dict[Key, typing.Any],
    right_dict: dict[typing.Any, Value],
) -> dict[Key, Value]:
    return {key: right_dict[type_key] for key, type_key in left_dict.items()}


__all__ = ("join_dicts",)
