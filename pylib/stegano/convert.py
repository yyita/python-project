from typing import (
    Iterable as _Iterable,
    Literal as _Literal,
    Generator as _Generator
)


def str_to_bits(
    string: str
) -> _Generator[_Literal[0, 1], None, None]:

    return (int(char) for char in string)


def bits_to_int(
    bits: _Iterable[_Literal[0, 1]]
) -> int:

    n = 0
    for bit in bits:
        n = (n << 1) | bit
    return n


def bytes_to_bits(
    bytes_: bytes | bytearray
) -> _Generator[_Literal[0, 1], None, None]:

    return (int(bit) for uint8 in bytes_ for bit in f'{uint8:08b}')