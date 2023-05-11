import math


class Building:
    def __init__(self, width, structure, height=2) -> None:
        self._height = height
        self._width = width
        self._type = structure  # T=triangular R =rectangle

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def type(self):
        return self._type

    @width.setter
    def type(self, value):
        self._type = value

    def print_triangular(self):
        if self._width % 2 == 0 or self._width > 2 * self._height:
            print("triangular is unprintable")
        else:
            spaces = (self._width - 1) // 2
            print(' ' * spaces, '*')
            spaces -= 1
            seq = list(range(3, self._width, 2))

            rep = (self._height - 2) // len(seq)
            left = self._height - 2 - rep * len(seq)
            for _ in range(left):
                print(' ' * spaces, '*' * seq[0])
            for element in seq:
                for _ in range(rep):
                    print(' ' * spaces, '*' * element)
                spaces -= 1
            print("", '*' * self._width)

    def triangular_info(self):
        option = int(
            input("what would you like to compute: for perimeter enter 1 for printing triangular enter something"))
        if option == 1:
            # perimeter
            c = math.sqrt((self._width // 2) ** 2 + self._height ** 2)
            print(self._width + 2 * c)
        else:
            self.print_triangular()

    def rectangle_info(self):

        print("Area: ", self._height * self._width) if (abs(self._height - self._width) > 5) else print("Perimeter: ", 2 * (
                    self._height + self._width))

    def information(self):
        if self._type == 'R':
            self.rectangle_info()
        else:
            self.triangular_info()
