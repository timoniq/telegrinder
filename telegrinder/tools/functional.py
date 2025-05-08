from fntypes.option import Nothing, Option, Some


def from_optional[Value](value: Value | None, /) -> Option[Value]:
    return Some(value) if value is not None else Nothing()


__all__ = ("from_optional",)
