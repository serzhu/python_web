from abc import ABC, abstractmethod
from enum import Enum

class TypeShape(str, Enum):
    circle = 'circle'
    square = 'square'


class Drawing(ABC):
    @abstractmethod
    def draw_shape(self, x, y, shape):
        pass

class DrawingRed(Drawing):
    def draw_shape(self, x, y, shape):
        print(f'Red Drawing a {shape} at ({x}, {y})')

class DrawingBlue(Drawing):
    def draw_shape(self, x, y, shape):
        print(f'Blue Drawing a {shape} at ({x}, {y})')
        
class  Shape(ABC):
    def __init__(self, x, y, drawing: Drawing):
        self.x = x
        self.y = y
        self.drawing = drawing

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        self.drawing.draw_shape(self.x, self.y, TypeShape.circle)

class Square(Shape):
    def draw(self):
        self.drawing.draw_shape(self.x, self.y, TypeShape.square)

if __name__ == '__main__':
    c = Circle(3,3,DrawingRed())
    s = Square(8,8,DrawingBlue())

    c.draw()
    s.draw()