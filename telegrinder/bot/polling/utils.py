def compute_number(
    default: int | float,
    input_value: int | float,
    conditional_value: int | float,
    /,
) -> int | float:
    return max(default, input_value) * (input_value <= conditional_value) + input_value * (
        input_value >= conditional_value
    )


__all__ = ("compute_number",)
