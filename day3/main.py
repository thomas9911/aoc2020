TREE = "#"
SQUARE = "■"


class Map:
    def __init__(self, input):
        self.data = [Map._parse_line(x) for x in input]

    def print(self):
        for x in self.data:
            for y in x:
                if y:
                    print(SQUARE, end="")
                else:
                    print(" ", end="")
            print()

    def expand(self, amount):
        self.data = [line * amount for line in self.data]

    def expand_till(self, max_right):
        rows = len(self.data)
        columns = len(self.data[0])

        magic_number = int((rows * max_right) / columns) + 1

        self.expand(magic_number)

    def count_trees(self, right, down):
        x = 0
        y = 0

        counter = 0

        for _ in range(0, len(self.data), down):
            if self.data[x][y]:
                counter += 1

            x += down
            y += right

        return counter

    @staticmethod
    def _parse_line(line):
        return [x == "#" for x in line]


with open("data.txt", "r") as f:
    data = f.read().splitlines()

    map = Map(data)

    map.expand_till(7)

    # map.print()

    amount = 1
    for (a, b) in [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]:
        counter = map.count_trees(a, b)
        print(counter)
        amount *= counter

    print(amount)
