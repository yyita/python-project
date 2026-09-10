import dataclasses
from pynput.mouse._win32 import Button as MouseButton
@dataclasses.dataclass
class MouseMoveEvent:
    """ 鼠标移动事件。 """
    x: int
    y: int
@dataclasses.dataclass
class MousePressEvent:
    """ 鼠标按下事件。 """
    x: int
    y: int
    button: MouseButton
@dataclasses.dataclass
class MouseReleaseEvent:
    """ 鼠标释放事件。 """
    x: int
    y: int
    button: MouseButton
@dataclasses.dataclass
class MouseScrollEvent:
    """ 鼠标滚动事件。 """
    x: int
    y: int
    dx: int
    dy: int