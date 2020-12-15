from collections import defaultdict


class Game:
    def __init__(self, init=[]):
        (data, index, last_number) = self._convert(init)
        self.data = data
        self.index = index
        self.last_number = last_number

    def next(self):
        num = None
        if len(self.data[self.last_number]) == 1:
            num = 0
        else:
            [second, last] = self.data[self.last_number]
            num = last - second

        if len(self.data[num]) == 0:
            self.data[num] = [self.index]
        else:
            x = self.data[num][-1]
            self.data[num] = [x, self.index]

        self.index += 1
        self.last_number = num
        return num

    @staticmethod
    def _convert(input):
        data = defaultdict(list)
        index = 0

        for item in input:
            data[item].append(index)
            index += 1

        return (data, index, item)


def main():
    with open("data.txt") as f:
        data = f.read().strip().split(",")
        numbers = [int(x) for x in data]

        g = Game(numbers)
        for _ in range(30000000 - len(numbers)):
            g.next()

        print(g.last_number)


if __name__ == "__main__":
    main()
