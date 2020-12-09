import itertools


def blep(input):
    index = 1
    while len(input) > index:
        yield input[0:index]
        index += 1


class Validator:
    N = 25

    def __init__(self):
        self.clear()

    def clear(self):
        self.buffer = Validator.N * [0]
        self.error = False
        self.last_input = []
        self.reset_indexes()

    def reset_indexes(self):
        self.index = Validator.N
        self.lower_index = 0

    def validate(self, input):
        self.last_input = input
        len_input = len(input)
        while self.index < len_input:
            self.buffer = input[self.lower_index : self.index]

            next_number = input[self.index]

            sums = (
                sum([a, b]) == next_number
                for (a, b) in itertools.permutations(self.buffer, 2)
            )
            valid = any(sums)
            if not valid:
                self.error = True
                return False

            self.index += 1
            self.lower_index += 1

    def find_weakness(self):
        if not self.error:
            return

        invalid_nmbr = self.invalid_number
        index = 0
        while True:
            input = self.last_input[index:]
            for item in blep(input):
                sum_item = sum(item)
                if sum_item == invalid_nmbr and len(item) >= 2:
                    return item
                if sum_item > invalid_nmbr:
                    index += 1
                    break

    @property
    def invalid_number(self):
        if self.error:
            return self.last_input[self.index]


with open("data.txt") as f:
    v = Validator()
    data = [int(x) for x in f.read().splitlines()]

    print("valid?:", v.validate(data))
    print("wrong nubmer:", v.invalid_number)
    weakness = v.find_weakness()
    print("weakness:", weakness)

    answer = sum([min(weakness), max(weakness)])
    print("answer:", answer)
