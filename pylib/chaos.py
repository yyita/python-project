def replace(
    bytes_,  # 支持 for 迭代，迭代项属于 uint8 。
    mapping256  # 0-255 => 0-255 映射表。
):  return bytearray(mapping256[uint8] for uint8 in bytes_)
def stream_xor(
    bytes_,
    stream
):  return bytearray(uint8_0 ^ uint8_1 for uint8_0, uint8_1 in zip(bytes_, stream))
def index_xor(
    bytes_
):  return bytearray(uint8 ^ (index % 256) for index, uint8 in enumerate(bytes_))
""" 环状单向异或（异步变换）。 """
def loop_one_way_xor_async(
    bytes_,
    step,
    is_reverse
):
    array = bytearray(bytes_)
    length = len(array)
    if not is_reverse:    range_ = range(length)
    else:                 range_ = reversed(range(length))
    for index in range_:
        array[index] ^= array[(index + step) % length]
    return array
""" 环状单向异或（同步变换）。 """
def loop_one_way_xor_sync(
    bytes_,
    step,
    is_reverse
):
    length = len(bytes_)
    if not is_reverse:    range_ = range(length)
    else:                 range_ = reversed(range(length))
    return bytearray((
        bytes_[index]
      ^ bytes_[(index + step) % length]
    ) for index in range_)
""" 环状双向异或（异步变换）。 """
# 输出与输入相同的预期输入：
# · x 长度是 step 的 2 倍。
# · 以 2 的 N 次幂为循环长度的循环，如：以 2（2 ** 1）为循环长度的 ABABAB 。
#   （循环单元的组成可重复，如：以 4（2 ** 2）为循环长度的 AAABAAAB ）。
def loop_two_way_xor_async(
    bytes_,
    step,
    is_reverse
):
    array = bytearray(bytes_)
    length = len(array)
    if not is_reverse:    range_ = range(length)
    else:                 range_ = reversed(range(length))
    for index in range_:
        array[index] ^= (
            array[(index - step) % length]
          ^ array[(index + step) % length]
        )
    return array
""" 环状双向异或（同步变换）。 """
def loop_two_way_xor_sync(
    bytes_,
    step,
    is_reverse
):
    length = len(bytes_)
    if not is_reverse:    range_ = range(length)
    else:                 range_ = reversed(range(length))
    return bytearray((
        bytes_[index]
      ^ bytes_[(index - step) % length]
      ^ bytes_[(index + step) % length]
    ) for index in range_)