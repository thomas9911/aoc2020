ROWS = 128
COLUMS = 8
ROWS_LENGTH = 7
COLUMNS_LENGTH = 3


def gen_seat_id(row, column):
    return 8 * row + column


def generate_func(left, right):
    def func(min, max, input, count=0):
        pin_point = int((max - min) / 2) + min
        try:
            if input[0] == left:
                return func(min, pin_point, input[1:], count + 1)
            if input[0] == right:
                return func(pin_point, max, input[1:], count + 1)
        except IndexError:
            pass
        return min, max, input, count

    return func


get_row = generate_func("F", "B")
get_column = generate_func("L", "R")


def parse(input):
    (row, _upper, input, count) = get_row(0, ROWS, input)
    if count == ROWS_LENGTH:
        (column, _upper, input, count) = get_column(0, COLUMS, input)
        if count == COLUMNS_LENGTH and input == "":
            return (row, column)
    raise "Failed"


if __name__ == "__main__":
    with open("data.txt", "r") as f:
        data = f.read().splitlines()
        data = [parse(x) for x in data]

        ids = [gen_seat_id(a, b) for (a, b) in data]

        left_overs = []
        for item in range(gen_seat_id(3, 0), gen_seat_id(ROWS - 1 - 3, COLUMS - 1) + 1):
            if item not in ids:
                left_overs.append(item)

        print(left_overs)
