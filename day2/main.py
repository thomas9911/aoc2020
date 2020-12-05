def parse_line(line):
    parts = line.split(" ")
    p1 = part_one(parts[0])
    p2 = part_two(parts[1])
    p3 = part_three(parts[2])
    return (p1, p2, p3)


def part_one(part):
    r = [int(x) for x in part.split("-")]
    return (r[0], r[1])


def part_two(part):
    return part.rstrip(":")


def part_three(part):
    return part


# def validate(p1, p2, p3):

#     count = p3.count(p2)
#     if p1[0] <= count <= p1[1]:
#         return True
#     return False


def check(input, char):
    return input == char


def validate(p1, p2, p3):
    (index_a, index_b) = p1

    x = check(p3[index_a - 1], p2)
    y = check(p3[index_b - 1], p2)
    return x ^ y


with open("data.txt", "r") as f:
    data = f.read().splitlines()

    counter = 0
    for item in data:
        (p1, p2, p3) = parse_line(item)

        # print(p3, calculate(p1, p2, p3))
        valid = validate(p1, p2, p3)
        if valid:
            counter += 1

    print(counter)
