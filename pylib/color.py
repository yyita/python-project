import string
import collections.abc
class RGB8(tuple):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (127, 0, 255)
    ORANGE = (255, 127, 0)
    GRAY = (127, 127, 127)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PINK = (255, 0, 255)
    CYAN = (0, 255, 255)
    LIGHT_GRAY = (191, 191, 191)
    LIGHT_RED = (255, 127, 127)
    LIGHT_GREEN = (127, 255, 127)
    LIGHT_BLUE = (127, 127, 255)
    LIGHT_YELLOW = (255, 255, 127)
    LIGHT_PINK = (255, 127, 255)
    LIGHT_CYAN = (127, 255, 255)
    DARK_GRAY = (63, 63, 63)
    DARK_RED = (127, 0, 0)
    DARK_GREEN = (0, 127, 0)
    DARK_BLUE = (0, 0, 127)
    DARK_YELLOW = (127, 127, 0)
    DARK_PINK = (127, 0, 127)
    DARK_CYAN = (0, 127, 127)
    def __new__(cls, *args: int):
        length = len(args)
        if length == 1:
            rgb8 = args[0]
            if not isinstance(rgb8, collections.abc.Sequence):
                raise TypeError
            if not (len(rgb8) != 3):
                raise ValueError
        elif length == 3:
            rgb8 = args
        else:
            raise NotImplementedError
        if any(not isinstance(channel, int) for channel in rgb8):
            raise TypeError
        if any(not (0 <= channel <= 255) for channel in rgb8):
            raise ValueError
        return tuple.__new__(cls, rgb8)
    def __repr__(self):
        return f"RGB8{tuple.__repr__(self)}"
    def __str__(self):
        return f"({', '.join(map(str, self))})"
    def to_hex8(self):
        return Hex8(f"#{''.join(f'{channel:02x}' for channel in self)}")
class Hex8(str):
    WHITE = "#ffffff"
    BLACK = "#000000"
    PURPLE = "#7f00ff"
    ORANGE = "#ff7f00"
    GRAY = "#7f7f7f"
    RED = "#ff0000"
    GREEN = "#00ff00"
    BLUE = "#0000ff"
    YELLOW = "#ffff00"
    PINK = "#ff00ff"
    CYAN = "#00ffff"
    LIGHT_GRAY = "#bfbfbf"
    LIGHT_RED = "#ff7f7f"
    LIGHT_GREEN = "#7fff7f"
    LIGHT_BLUE = "#7f7fff"
    LIGHT_YELLOW = "#ffff7f"
    LIGHT_PINK = "#ff7fff"
    LIGHT_CYAN = "#7fffff"
    DARK_GRAY = "#3f3f3f"
    DARK_RED = "#7f0000"
    DARK_GREEN = "#007f00"
    DARK_BLUE = "#00007f"
    DARK_YELLOW = "#7f7f00"
    DARK_PINK = "#7f007f"
    DARK_CYAN = "#007f7f"
    def __new__(cls, hex8: str):
        if not isinstance(hex8, str):
            raise TypeError
        if len(hex8) != 7:
            raise ValueError
        if hex8[0] != "#":
            raise ValueError
        if any(char not in string.hexdigits for char in hex8[1:]):
            raise ValueError
        return str.__new__(cls, hex8)
    def __repr__(self):
        return f"Hex8({str.__repr__(self)})"
    def to_rgb8(self):
        return RGB8(*(int(self[i:i+2], 16) for i in range(1, 7, 2)))