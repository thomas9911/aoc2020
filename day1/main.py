def check(data):
    for a in data:
        for b in data:
            # if a + b == 2020:
            #     return a, b, a * b
            for c in data:
                if a + b + c == 2020:
                    return a, b, c, a * b * c


with open("data.txt", "r") as f:
    data = f.read().splitlines()
    data = [int(x) for x in data]

    res = check(data)

    print(res)
