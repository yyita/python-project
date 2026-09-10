from PIL import Image as _Image
from itertools import chain as _chain
from typing import (
    Generator as _Generator,
    Literal as _Literal
)
from stegano.convert import (
    str_to_bits as _str_to_bits,
    bits_to_int as _bits_to_int,
    bytes_to_bits as _bytes_to_bits
)
from stegano.validate import bit_validate as _bit_validate


_channel_count = {"RGB": 3, "RGBA": 4}
_mode_range = {"RGB", "RGBA"}


def _modify_last(
    image: _Image.Image,
    bits: _Generator[_Literal[0, 1], None, None],
    *,
    only_opaque: bool = False
) -> None:

    width, height = image.size
    access = image.load()

    for y in range(height):
        for x in range(width):

            pixel = list(access[x, y])

            if only_opaque and pixel[3] == 0:
                continue

            try:
                for j, channel in enumerate(pixel):
                    bit = _bit_validate(next(bits))
                    pixel[j] ^= (channel & 1) ^ bit
            except StopIteration:            return
            finally:    access[x, y] = tuple(pixel)


def _extract_bits(
    image: _Image.Image,
    size: int,
    *,
    start = 0,
    only_opaque: bool = False
) -> _Generator[_Literal[0, 1], None, None]:

    width, height = image.size
    i = 0
    k = size + start
    access = image.load()

    for y in range(height):
        for x in range(width):

            pixel = access[x, y]

            if only_opaque and pixel[3] == 0:
                continue

            for channel in pixel:
                if i >= start:
                    yield channel & 1
                i += 1
                if i >= k:    return


def hide(
    image: _Image.Image,
    added: bytes | _Generator[_Literal[0, 1], None, None],
    *,
    only_opaque = False
) -> _Image.Image:

    mode = image.mode

    if (mode not in _mode_range):    raise NotImplementedError
    if isinstance(added, bytes):        added = tuple(_bytes_to_bits(added))

    width, height = image.size
    capacity = width * height * _channel_count[mode]

    length_of_sign = (capacity - 1).bit_length()
    length_of_added = len(added)

    sign = _str_to_bits(f"{length_of_added:0{length_of_sign}b}")
    bits = _chain(sign, added)

    _modify_last(image, bits, only_opaque = only_opaque)

    try:
        next(bits)
        raise OverflowError(len(tuple(bits)) + 1)
    except StopIteration:
        pass


def find(
    image: _Image.Image,
    *,
    only_opaque = False
) -> _Generator[_Literal[0, 1], None, None]:

    mode = image.mode
    if (mode not in _mode_range):    raise NotImplementedError

    width, height = image.size
    capacity = width * height * _channel_count[mode]
    length_of_sign = (capacity - 1).bit_length()

    sign_bits = _extract_bits(
        image,
        size = length_of_sign,
        only_opaque = only_opaque
    )
    extracted_size = _bits_to_int(sign_bits)
    return _extract_bits(
        image,
        size = extracted_size,
        start = length_of_sign,
        only_opaque = only_opaque
    )