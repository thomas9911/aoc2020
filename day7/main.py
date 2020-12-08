# import re

syntax = "[color] bags contain ([amount] [color]s?|,)+."


class RuleBook:
    def __init__(self, input):
        rules = {}
        for line in input.splitlines():
            (key, value) = parse_line(line)
            rules[key] = value
        self.rules = rules

    def can_contain(self, color):


        colors = self._find_direct(color)
        z = [self.can_contain(x) for x in colors]
        b = [x for y in z for x in y]

        colors.extend(b)
        colors = list(set(colors))

        return colors

    def _find_direct(self, color):
        keys = []
        for (k, rules) in self.rules.items():
            found = [x for x in rules if x["color"] == color]
            if found:
                keys.append(k)
        return keys

    def lookup(self, color):
        if color is None:
            return []
        
        bags = []
        rule = self.rules[color]
        for sub_rule in rule:
            sub_color = sub_rule["color"]
            sub_amount = sub_rule["amount"]
            if sub_color is not None:
                bags.extend([sub_color]*sub_amount)
                bags.extend(sub_amount*self.lookup(sub_color))
        
        return bags

def parse_line(input):
    [left, rest] = input.split("bags contain")
    left = left.strip()
    right = [parse_right(x) for x in rest.split(",")]
    return (left, right)


def parse_right(input):
    [amount, color] = (
        input.replace(".", "")
        .replace("bags", "")
        .replace("bag", "")
        .strip()
        .split(" ", 1)
    )
    if amount == "no" and color == "other":
        return {"amount": 0, "color": None}
    return {"amount": int(amount), "color": color}


# regex = re.compile(r"^(?P<left>[\w ]*)")

with open("data.txt") as f:
    data = f.read()
    book = RuleBook(data)

    # # part a
    # colors = book.can_contain("shiny gold")
    # print(len(colors))

    # # part b
    bags = book.lookup("shiny gold")
    print(len(bags))
