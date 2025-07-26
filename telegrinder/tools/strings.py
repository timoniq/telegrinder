def to_utf16_map(s: str, /) -> list[int]:
    utf16_map = list[int]()
    utf16_pos = 0

    for char in s:
        utf16_map.append(utf16_pos)
        utf16_len = len(char.encode("utf-16-le")) // 2
        utf16_pos += utf16_len

    utf16_map.append(utf16_pos)
    return utf16_map


def utf16_to_py_index(utf16_map: list[int], utf16_index: int, /) -> int:
    for index, u in enumerate(utf16_map):
        if u >= utf16_index:
            return index

    return len(utf16_map) - 1


__all__ = ("to_utf16_map", "utf16_to_py_index")
