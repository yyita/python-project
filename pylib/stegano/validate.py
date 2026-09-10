def bit_validate(
    x
) -> bool:

    if not isinstance(x, int):
        raise TypeError(type(x))
    if not (0 <= x <= 1):
        raise ValueError(x)
    return x