from apps.shape.types import ShapeTypeAbstract


class Rectangle(ShapeTypeAbstract):
    """ This is an equilateral triangle"""
    parameters = ['length_1', 'width_1']

    def area(self):
        return self.length_1 * self.width_1

    def perimeter(self):
        return 2 * (self.length_1 + self.width_1)
