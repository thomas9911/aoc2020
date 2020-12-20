from enum import Enum
import itertools
from collections import defaultdict
from pprint import pprint

class State(Enum):
    on = "#"
    off = "."

class SlicableDictError(Exception):
    pass

class SlicableDict(dict):
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._do_slicing(key)
        else:
            return super().__getitem__(key)

    def _do_slicing(self, key):
        if key.start and key.stop:
            r = range(key.start, key.stop, key.step or 1)
        else:
            raise KeyError(key)

        return [v for (k, v) in self.items() if k in r]


class DefaultSlicableDict(SlicableDict):
    def __init__(self):
        self.locked = False
        super().__init__()

    def set_locked(self):
        self.locked = True

    def unset_locked(self):
        self.locked = False

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            if not self.locked:
                self[key] = DefaultSlicableDict()
                return self.__getitem__(key)
            else:
                return super().__getitem__(key) 


class Grid:
    def __init__(self):
        self.space = DefaultSlicableDict()
        self.previous_space = None
        self.x = (0, 0)
        self.y = (0, 0)
        self.z = (0, 0)


    def insert(self, x, y, z, value):
        self.space[x][y][z] = value
        if x < self.x[0]:
            self.x = (x, self.x[1])
        if x > self.x[1]:
            self.x = (self.x[0], x)

        if y < self.y[0]:
            self.y = (y, self.y[1])
        if y > self.y[1]:
            self.y = (self.y[0], y)

        if z < self.z[0]:
            self.z = (z, self.z[1])
        if z > self.z[1]:
            self.z = (self.z[0], z)

    def load(self, data):
        z = 0
        for (x, line) in enumerate(data):
            for (y, item) in enumerate(line):
                self.insert(x, y, z, item)

    def iter(self):
        self.space.set_locked()
        for (x, xas) in self.space.items():
            xas.set_locked()
            for (y, yas) in xas.items():
                yas.set_locked()
                for (z, zas) in yas.items():
                    yield (x, y, z, zas)
                yas.unset_locked()
            xas.unset_locked()
        self.space.unset_locked()
            
    def next(self):
        next_space = Grid()

        for (x, y, z, item) in self.iter():
            # print(x, y, z, item)
            counter = defaultdict(int)
            for (a, b, c) in neighbour_iter():
                try:
                    this = self.space[x+a][y+b][z+c] or State.off
                    counter[this] += 1
                    # print(self.space[x+a][y+b][z+c])
                except KeyError:
                    pass

            new_item = State.off
            if item == State.on:
                if counter[State.on] in [2, 3]:
                    new_item = State.on
                else:
                    pass
            elif item == State.off: 
                if counter[State.on] == 3:
                    new_item = State.on

            next_space.insert(x, y, z, new_item)

        next_space.print_details()


    def print_details(self):
        pprint(self.space)
        print(self.x)
        print(self.y)
        print(self.z) 


def neighbour_iter():
    return itertools.product(*[range(-1, 2)] * 3)


def ok(x, y, z):
    for (a, b, c) in neighbour_iter():
        if (a, b, c) == (x, y, z):
            continue

        print(a, b, c)


# itertools.product(range(-1, 2), range(-1, 2))

def parse_text(text):
    return [[State(x) for x in lines] for lines in text.splitlines()]


# def load_grid(grid, data):



def main():
    with open("data.txt") as f:
        data = f.read()

        data = parse_text(data)
        # print(data)

        # ok(1,1,1)

        # s = SlicableDict()
        # s[-2] = 1
        # s[-1] = 5
        # s[0] = 6
        # s[1] = 8
        # s[2] = 11
        # s[3] = 15
        # s[4] = 18

        # print(s[1:2])

        g = Grid()
        g.load(data)
        # g.print_details()

        g.next()
        g.next()
        g.next()
        g.next()

        # g.space[1][2][3] = 1

        # g.insert(1,2,3, "kaas")
        # g.insert(-5,1,6, "baas")



if __name__ == "__main__":
    main()
