from enum import Enum
from pprint import pprint
import itertools
import multiprocessing as mp


class Seat(Enum):
    EMPTY = "L"
    FLOOR = "."
    OCCUPIED = "#"


class Direction(Enum):
    NORTH = "N"
    NORTH_EAST = "NE"
    EAST = "E"
    SOUTH_EAST = "SE"
    SOUTH = "S"
    SOUTH_WEST = "SW"
    WEST = "W"
    NORTH_WEST = "NW"

    def generate_indexes(self, start_x, start_y):
        if Direction.NORTH == self:
            while True:
                start_x -= 1
                yield (start_x, start_y)

        if Direction.NORTH_EAST == self:
            while True:
                start_x -= 1
                start_y += 1
                yield (start_x, start_y)

        if Direction.EAST == self:
            while True:
                start_y -= 1
                yield (start_x, start_y)

        if Direction.SOUTH_EAST == self:
            while True:
                start_x += 1
                start_y += 1
                yield (start_x, start_y)

        if Direction.SOUTH == self:
            while True:
                start_x += 1
                yield (start_x, start_y)

        if Direction.SOUTH_WEST == self:
            while True:
                start_x += 1
                start_y -= 1
                yield (start_x, start_y)

        if Direction.WEST == self:
            while True:
                start_y += 1
                yield (start_x, start_y)

        if Direction.NORTH_WEST == self:
            while True:
                start_x -= 1
                start_y -= 1
                yield (start_x, start_y)


class Ferry:
    def __init__(self, text):
        seats = Ferry.parse_seats(text)
        self.seats = seats
        self.prev_seats = None
        self.rounds = 0
        self.rows = len(seats)
        self.columns = len(seats[0])
        self.solution = "b"

    def __eq__(self, other):
        return self.seats == other.seats

    def __str__(self):
        return "\n".join(["".join([x.value for x in rows]) for rows in self.seats])

    @property
    def all_seats(self):
        return [x for y in self.seats for x in y]

    @staticmethod
    def parse_seats(text):
        lines = text.splitlines()
        seats = [[Seat(field) for field in line] for line in lines]
        return seats

    def adjacent_seats(self, x, y):
        seats = []
        for (i, j) in itertools.product(range(-1, 2), range(-1, 2)):
            new_x = x + i
            new_y = y + j
            if new_x < 0 or new_x >= self.rows:
                continue
            if new_y < 0 or new_y >= self.columns:
                continue
            if new_x == x and new_y == y:
                continue

            seats.append((new_x, new_y, self.seats[new_x][new_y]))

        return seats

    def in_sight_seats(self, x, y):
        seats = []
        for direction in Direction:
            for (a, b) in direction.generate_indexes(x, y):
                if a < 0 or b < 0:
                    break

                try:
                    if self.seats[a][b] != Seat.FLOOR:
                        seats.append(self.seats[a][b])
                        break
                except IndexError:
                    break

        return seats

    @staticmethod
    def gen_board(rows, columns):
        return [[Seat.FLOOR for _ in range(columns)] for _ in range(rows)]

    def next_board(self):
        new_board = self.gen_board(self.rows, self.columns)

        if self.solution == "b":
            func = self.next_seat_b
        else:
            func = self.next_seat_a

        with mp.Pool(processes=4) as pool:
            result = pool.starmap(
                func, itertools.product(range(self.rows), range(self.columns))
            )

        for (row, column, seat) in result:
            new_board[row][column] = seat

        return new_board

    def update_board(self):
        self.prev_seats = self.seats
        self.seats = self.next_board()
        self.rounds += 1

    def update_until_no_change(self):
        same = False
        while not same:
            self.update_board()
            same = self.seats == self.prev_seats

    def next_seat_a(self, row, column):
        stats = self.seats_stats(self.adjacent_seats(row, column))
        current_seat = self.seats[row][column]

        if current_seat == Seat.EMPTY and stats[Seat.OCCUPIED] == 0:
            return (row, column, Seat.OCCUPIED)

        if current_seat == Seat.OCCUPIED and stats[Seat.OCCUPIED] >= 4:
            return (row, column, Seat.EMPTY)

        return (row, column, current_seat)

    def next_seat_b(self, row, column):
        stats = self.seats_stats(self.in_sight_seats(row, column))
        current_seat = self.seats[row][column]

        if current_seat == Seat.EMPTY and stats[Seat.OCCUPIED] == 0:
            return (row, column, Seat.OCCUPIED)

        if current_seat == Seat.OCCUPIED and stats[Seat.OCCUPIED] >= 5:
            return (row, column, Seat.EMPTY)

        return (row, column, current_seat)

    @staticmethod
    def seats_stats(seats):
        if isinstance(seats[0], tuple):
            seats = [seat for (_, _, seat) in seats]

        data = {x: 0 for x in Seat}
        for seat in seats:
            data[seat] += 1
        return data


def main():
    with open("data.txt") as f:
        text = f.read()
        p = Ferry(text)
        # p.solution = "a"

        p.next_board()

        p.update_until_no_change()

        print(p.seats_stats(p.all_seats))


def test_next_board():
    text = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

    text2 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

    p = Ferry(text)
    p.seats = p.next_board()

    q = Ferry(text2)

    assert p == q
    assert str(p) == str(q)


if __name__ == "__main__":
    test_next_board()
    main()
