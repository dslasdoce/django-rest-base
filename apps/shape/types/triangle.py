from apps.shape.types import ShapeTypeAbstract


class Triangle(ShapeTypeAbstract):
    """ This is an equilateral triangle"""
    parameters = ['length']

    def area(self):
        base = self.length / 2
        height = base ** 0.5
        return 0.5 * base * height

    def perimeter(self):
        return 3 * self.length
