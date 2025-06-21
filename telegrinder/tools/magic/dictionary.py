import typing


def join_dicts[Key: typing.Hashable, Value](
    left_dict: dict[Key, typing.Any],
    right_dict: dict[typing.Any, Value],
    /,
) -> dict[Key, Value]:
    return {left_key: right_dict[right_key] for left_key, right_key in left_dict.items()}


def extract[Key: typing.Hashable, Value](
    keys: typing.Iterable[Key],
    mapping: typing.Mapping[Key, Value],
    /,
) -> dict[Key, Value]:
    return {key: mapping[key] for key in keys if key in mapping}


__all__ = ("extract", "join_dicts")
