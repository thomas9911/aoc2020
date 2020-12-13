import multiprocessing as mp


def run_a(my_time, ids):
    (a, b) = find_next_bus(my_time, ids)
    print((a - my_time) * b)


def find_next_bus(my_time, ids):
    start = my_time
    while True:
        for id in ids:
            if start % id == 0:
                return (start, id)
        start += 1


# nicely stolen


from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        print(n_i)
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


# nicely stolen


def check(iterator, index):
    return all((index % b == (-a % b) for (a, b) in iterator))


def brute_force(text):
    # t % 7 == 0 % 7
    # t % 13 == -1 % 13
    # t % 59 == -4 % 59
    asdf = [(index, int(id)) for (index, id) in enumerate(text.split(",")) if id != "x"]

    index = 100000000000000
    batch_size = 5000000
    processes = 8
    chunksize = batch_size // 8

    with mp.Pool(processes) as pool:
        while True:
            batch = [(asdf, i) for i in range(index, index + batch_size)]
            results = pool.starmap(check, batch, chunksize=chunksize)
            if any(results):
                return index + [a for (a, b) in enumerate(results) if b == True][0]
            else:
                index += batch_size


def print_model(text):
    iterator = [
        (index, int(id)) for (index, id) in enumerate(text.split(",")) if id != "x"
    ]
    iterator = sorted(iterator, key=lambda x: x[1], reverse=True)

    for (a, b) in iterator:
        print(f"t % {b} == {-a % b} % {b}")


def calculate(text):
    iterator = [
        (index, int(id)) for (index, id) in enumerate(text.split(",")) if id != "x"
    ]
    a = []
    n = []
    for (x, y) in sorted(iterator, key=lambda x: x[1], reverse=False):
        a.append(-x % y)
        n.append(y)

    return chinese_remainder(n, a)


def main():
    with open("data.txt") as f:
        data = f.read().splitlines()

        # print(brute_force(data[1]))
        # print_model(data[1])
        # my_time = int(data[0])
        # ids = [int(x) for x in data[1].split(",") if x != "x"]

        # run_a(my_time, ids)

        print(calculate(data[1]))


if __name__ == "__main__":
    main()
