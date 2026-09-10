import math
import itertools
import abc
import os
import time
class Stateless(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def randbytes(cls, size):
        raise NotImplementedError
    @classmethod
    def randbits(cls, size):
        return int.from_bytes( cls.randbytes( math.ceil(size / 8) ) ) & (1 << size) - 1
    @classmethod
    def randint(cls, minimum: int, maximum: int):
        delta = maximum - minimum
        byte_size = math.ceil(delta.bit_length() / 8)
        while True:
            n = int.from_bytes(cls.randbytes(byte_size))
            if n <= delta:
                break
        return minimum + n
    @classmethod
    def randfloat(cls):
        return cls.randint(0, 1 << 32) / (1 << 32)
    @classmethod
    def select(cls, items, n = 1):
        cap = len(items) - 1
        return [items[cls.randint(0, cap)] for _ in itertools.repeat(None, n)]
    @classmethod
    def reorder(cls, items):
        state = list(items)
        for i1 in reversed(range(1, len(state))):
            i2 = cls.randint(0, i1)
            state[i1], state[i2] = state[i2], state[i1]
        return state
    @classmethod
    def sample(cls, items, n):
        state = list(items)
        return [state.pop(cls.randint(0, len(state) - 1)) for _ in itertools.repeat(None, n)]
class Urandom(Stateless):
    @classmethod
    def randbytes(cls, size):
        return os.urandom(size)
class Time(Stateless):
    @classmethod
    def randbytes(cls, size):
        array = bytearray()
        for _ in itertools.repeat(None, size):
            while True:
                # 从右往左数，取第 3 到第 6 个数位上的数，总长为 4 ，一万种可能性。
                # 不取其他位置上的数，是它们短期内变化幅度太小，不适合作为熵源。
                # 当然，也不排除在更高性能的计算机上这几位也不适合的可能。
                n = (time.perf_counter_ns() // 10 ** 2) % 10 ** 4
                if n <= 9984:
                    break
            array.append(n % 256)
        return bytes(array)