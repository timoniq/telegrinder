import re

PATTERN = re.compile(r"[^ a-z A-Z 0-9 \s]")


def to_pascal_case(string: str, /) -> str:
    return "".join(
        "".join(char.capitalize() for char in sub_str)
        for sub_str in (char.split() for char in PATTERN.split(string))
    )


__all__ = ("to_pascal_case",)
