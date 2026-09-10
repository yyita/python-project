import abc
import math
class Graphics(abc.ABC):
    """ 图形 """
class Polygon(Graphics):
    """ 封闭图形 """
    @abc.abstractmethod
    def area(self): ...
    @abc.abstractmethod
    def perimeter(self): ...
class Triangle(Polygon):
    """ 三角形 """
    __slots__ = ("side_a", "side_b", "side_c")
    def __init__(self, side_a, side_b, side_c):
        if side_a <= 0:
            raise ValueError
        if side_b <= 0:
            raise ValueError
        if side_c <= 0:
            raise ValueError
        if any(
            (side_a + side_b <= side_c),
            (side_a + side_c <= side_b), 
            (side_b + side_c <= side_a)
        ):
            raise ValueError
        super().__init__()
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
    def __repr__(self):
        return f"Triangle({self.side_a}, {self.side_b}, {self.side_c})"
    def area(self):
        p = (self.side_a + self.side_b + self.side_c) / 2
        return math.sqrt(p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c))
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c
class Rectangle(Polygon):
    """ 矩形 """
    __slots__ = ("width", "height")
    def __init__(self, width, height):
        if width <= 0:
            raise ValueError
        if height <= 0:
            raise ValueError
        super().__init__()
        self.width = width
        self.height = height
    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"
    def area(self):
        return self.width * self.height
    def perimeter(self):
        return 2 * (self.width + self.height)
    def diagonal(self):
        return math.hypot(self.width, self.height)
class Square(Rectangle):
    """ 正方形 """
    __slots__ = ("width", "height")
    def __init__(self, length):
        if length <= 0:
            raise ValueError
        super().__init__(length, length)
    def __repr__(self):
        return f"Square({self.width})"
    def perimeter(self):
        return 4 * self.width
class Circle(Polygon):
    """ 圆 """
    __slots__ = ("radius", "diameter")
    def __init__(self, *, radius = None, diameter = None):
        if radius is None:
            if diameter is None:
                self.radius = 0.5
                self.diameter = 1.0
            else:
                self.radius = diameter / 2
                self.diameter = diameter
        elif diameter is None:
            self.radius = radius
            self.diameter = radius * 2
        elif radius * 2 == diameter:
            self.radius = radius
            self.diameter = diameter
        else:
            raise ValueError
        super().__init__()
    def __repr__(self):
        return f"Circle(radius={self.radius}, diameter={self.diameter})"
    @staticmethod
    def from_radius(value):
        return Circle(radius=(value * 2))
    @staticmethod
    def from_diameter(value):
        return Circle(diameter=value)
    def area(self):
        return math.pi * (self.radius ** 2)
    def perimeter(self):
        return math.pi * self.diameter
    circumference = perimeter
class Cuboid:
    """ 长方体 """
    __slots__ = ("length", "width", "height")
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
    def __repr__(self):
        return f"Cuboid({self.length}, {self.width}, {self.height})"
    def area(self):
        return (2 * (self.length * self.width) + 
                2 * (self.length * self.height) + 
                2 * (self.width * self.height))
    def volume(self):
        return self.length * self.width * self.height
    def diagonal(self):
        return math.hypot(self.length, self.width, self.height)
class Cube(Cuboid):
    """ 正方体 """
    __slots__ = ("length", "width", "height")
    def __init__(self, length):
        super().__init__(length, length, length)
    def __repr__(self):
        return f"Cube({self.length})"
    def area(self):
        return 6 * (self.length * self.length)
    def volume(self):
        return self.length * self.length * self.length
    def diagonal(self):
        return math.cbrt(3) * self.length
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"
    def distance(self, other: 'Point2D'):
        return math.hypot(abs(self.x - other.x),
                          abs(self.y - other.y))
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"
    def distance(self, other: 'Point3D'):
        return math.hypot(abs(self.x - other.x),
                          abs(self.y - other.y),
                          abs(self.z - other.z))
class Position2D(Point2D):
    def __init__(self, x, y):
        super().__init__(x, y)
    def __repr__(self):
        return f"Position2D({self.x}, {self.y})"
class Position3D(Point3D):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
    def __repr__(self):
        return f"Position3D({self.x}, {self.y}, {self.z})"