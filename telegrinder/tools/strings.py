import typing

type Index = int
type UTF16Length = int
type UTF16Map = typing.Sequence[UTF16Length]


def is_utf8_character_first_code_unit(char: int, /) -> bool:
    return (char & 0xC0) != 0x80


def utf8_utf16_length(string: str, /) -> UTF16Length:
    length = 0

    for char in string:
        length += is_utf8_character_first_code_unit(c := ord(char)) + ((c & 0xF8) == 0xF0)

    return length


def to_utf16_map(s: str, /) -> UTF16Map:
    utf16_map = list[int]()
    utf16_pos = 0

    for char in s:
        utf16_map.append(utf16_pos)
        utf16_pos += utf8_utf16_length(char)

    utf16_map.append(utf16_pos)
    return utf16_map


def utf16_to_py_index(utf16_map: UTF16Map, utf16_index: Index, /) -> Index:
    for index, u in enumerate(utf16_map):
        if u >= utf16_index:
            return index

    return len(utf16_map) - 1


__all__ = ("to_utf16_map", "utf8_utf16_length", "utf16_to_py_index")
