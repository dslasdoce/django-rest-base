from apps.shape.types import ShapeTypeAbstract


class Square(ShapeTypeAbstract):
    """ This is an equilateral triangle"""
    parameters = ['length_1']

    def area(self):
        return self.length_1 * self.length_1

    def perimeter(self):
        return 4 * self.length_1
