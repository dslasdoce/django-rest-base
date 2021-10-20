from apps.shape.types import ShapeTypeAbstract


class Triangle(ShapeTypeAbstract):
    """ This is an equilateral triangle"""
    parameters = ['length_1', 'length_2', 'length_3']

    def area(self):
        semi_perimeter = 0.5 * (self.length_1 + self.length_2 + self.length_3)
        return (
            (
                semi_perimeter
                * (semi_perimeter - self.length_1)
                * (semi_perimeter - self.length_2)
                * (semi_perimeter - self.length_3)
            ) ** 0.5
        )

    def perimeter(self):
        return self.length_1 + self.length_2 + self.length_3
