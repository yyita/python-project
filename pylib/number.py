'''
限制值的范围。
示例:
>>> clamp(100-200, minimum=0, maximum=100)
0
>>> clamp(100+50, minimum=0, maximum=100)
100
'''
def clamp(
    value,
    minimum,
    maximum
):  return max(min(value, maximum), minimum)
'''
求余，但不同的是你可以指定最小值。
示例:
>>> mod(1, minimum=1, maximum=7)
1
>>> mod(7+1, minimum=1, maximum=7)
1
'''
def mod(
    value,
    minimum,
    maximum
):  return minimum + (value - minimum) % (maximum - minimum + 1)
'''
获取任意位置的 bit 。
示例:
>>> get_bits(1, 0)
1
>>> get_bits(1, 1)
0
'''
def get_bit(
    n: int,
    i: int
):  return n >> i & 1
class ClampInt(int):
    def __new__(cls, value: int, minimum: int, maximum: int):
        cls.minimum = minimum
        cls.maximum = maximum
        return super().__new__(cls, clamp(value, minimum, maximum))
    @classmethod
    def clamp(cls, value):
        return ClampInt(value, cls.minimum, cls.maximum)
    def __add__(cls, value):
        return cls.clamp(super().__add__(value))
    def __radd__(cls, value):
        return cls.clamp(super().__radd__(value))
    def __sub__(cls, value):
        return cls.clamp(super().__sub__(value))
    def __rsub__(cls, value):
        return cls.clamp(super().__rsub__(value))
    def __mul__(cls, value):
        return cls.clamp(super().__mul__(value))
    def __rmul__(cls, value):
        return cls.clamp(super().__rmul__(value))
    def __truediv__(cls, value):
        return cls.clamp(super().__truediv__(value))
    def __rtruediv__(cls, value):
        return cls.clamp(super().__rtruediv__(value))
    def __floordiv__(cls, value):
        return cls.clamp(super().__floordiv__(value))
    def __rfloordiv__(cls, value):
        return cls.clamp(super().__rfloordiv__(value))
    def __mod__(cls, value):
        return cls.clamp(super().__mod__(value))
    def __rmod__(cls, value):
        return cls.clamp(super().__rmod__(value))
    def __divmod__(cls, value):
        return cls.clamp(super().__divmod__(value))
    def __rdivmod__(cls, value):
        return cls.clamp(super().__rdivmod__(value))
    def __pow__(cls, value):
        return cls.clamp(super().__pow__(value))
    def __rpow__(cls, value):
        return cls.clamp(super().__rpow__(value))
    def __neg__(cls):
        return cls.clamp(super().__neg__())
    def __pos__(cls):
        return cls.clamp(super().__pos__())
    def __abs__(cls):
        return cls.clamp(super().__abs__())
    def __invert__(cls):
        return cls.clamp(super().__invert__())
    def __or__(cls, value):
        return cls.clamp(super().__or__(value))
    def __ror__(cls, value):
        return cls.clamp(super().__ror__(value))
    def __and__(cls, value):
        return cls.clamp(super().__and__(value))
    def __rand__(cls, value):
        return cls.clamp(super().__rand__(value))
    def __xor__(cls, value):
        return cls.clamp(super().__xor__(value))
    def __rxor__(cls, value):
        return cls.clamp(super().__rxor__(value))
    def __lshift__(cls, value):
        return cls.clamp(super().__lshift__(value))
    def __rlshift__(cls, value):
        return cls.clamp(super().__rlshift__(value))
    def __rshift__(cls, value):
        return cls.clamp(super().__rshift__(value))
    def __rrshift__(cls, value):
        return cls.clamp(super().__rrshift__(value))
    def __round__(cls, ndigits = ...):
        return cls.clamp(super().__round__(ndigits))
    def __ceil__(cls):
        return cls.clamp(super().__ceil__())
    def __floor__(cls):
        return cls.clamp(super().__floor__())
    def __trunc__(cls):
        return cls.clamp(super().__trunc__())
    def __repr__(self):
        return f"ClampInt({super().__repr__()})"
    def __str__(self):
        return f"{int(self)}"
class ModInt(int):
    def __new__(cls, value: int, minimum: int, maximum: int):
        cls.minimum = minimum
        cls.maximum = maximum
        return super().__new__(cls, mod(value, cls.minimum, cls.maximum))
    @classmethod
    def mod(cls, value):
        return ModInt(value, cls.minimum, cls.maximum)
    def __add__(cls, value):
        return cls.mod(super().__add__(value))
    def __radd__(cls, value):
        return cls.mod(super().__radd__(value))
    def __sub__(cls, value):
        return cls.mod(super().__sub__(value))
    def __rsub__(cls, value):
        return cls.mod(super().__rsub__(value))
    def __mul__(cls, value):
        return cls.mod(super().__mul__(value))
    def __rmul__(cls, value):
        return cls.mod(super().__rmul__(value))
    def __truediv__(cls, value):
        return cls.mod(super().__truediv__(value))
    def __rtruediv__(cls, value):
        return cls.mod(super().__rtruediv__(value))
    def __floordiv__(cls, value):
        return cls.mod(super().__floordiv__(value))
    def __rfloordiv__(cls, value):
        return cls.mod(super().__rfloordiv__(value))
    def __mod__(cls, value):
        return cls.mod(super().__mod__(value))
    def __rmod__(cls, value):
        return cls.mod(super().__rmod__(value))
    def __divmod__(cls, value):
        return cls.mod(super().__divmod__(value))
    def __rdivmod__(cls, value):
        return cls.mod(super().__rdivmod__(value))
    def __pow__(cls, value):
        return cls.mod(super().__pow__(value))
    def __rpow__(cls, value):
        return cls.mod(super().__rpow__(value))
    def __neg__(cls):
        return cls.mod(super().__neg__())
    def __pos__(cls):
        return cls.mod(super().__pos__())
    def __abs__(cls):
        return cls.mod(super().__abs__())
    def __invert__(cls):
        return cls.mod(super().__invert__())
    def __or__(cls, value):
        return cls.mod(super().__or__(value))
    def __ror__(cls, value):
        return cls.mod(super().__ror__(value))
    def __and__(cls, value):
        return cls.mod(super().__and__(value))
    def __rand__(cls, value):
        return cls.mod(super().__rand__(value))
    def __xor__(cls, value):
        return cls.mod(super().__xor__(value))
    def __rxor__(cls, value):
        return cls.mod(super().__rxor__(value))
    def __lshift__(cls, value):
        return cls.mod(super().__lshift__(value))
    def __rlshift__(cls, value):
        return cls.mod(super().__rlshift__(value))
    def __rshift__(cls, value):
        return cls.mod(super().__rshift__(value))
    def __rrshift__(cls, value):
        return cls.mod(super().__rrshift__(value))
    def __round__(cls, ndigits = ...):
        return cls.mod(super().__round__(ndigits))
    def __ceil__(cls):
        return cls.mod(super().__ceil__())
    def __floor__(cls):
        return cls.mod(super().__floor__())
    def __trunc__(cls):
        return cls.mod(super().__trunc__())
    def __repr__(self):
        return f"ModInt({super().__repr__()})"
    def __str__(self):
        return f"{int(self)}"