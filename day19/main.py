from dataclasses import dataclass
from typing import Union

from functools import lru_cache
import inspect
import sys

# import resource, sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
# sys.setrecursionlimit(5000)

from itertools import count

def stack_size2a(size=2):
    """Get stack size for caller's frame.
    """
    frame = sys._getframe(size)

    for size in count(size):
        frame = frame.f_back
        if not frame:
            return size



@dataclass
class Value:
    value: str


@dataclass
class Option:
    indexes: [int]


@dataclass
class SubRule:
    options: [Option]


@dataclass
class Rule:
    index: int
    value: Union[SubRule, Value]


# @dataclass
class RuleBook:
    # rules: [Rule]

    # def map(self):
    #     return {rule.index: rule.value for rule in self.rules}
    def __init__(self, rules: [Rule]):
        self.book = {rule.index: rule.value for rule in rules}

    def matches(self, input):
        answer = self._matches(input, 0)
        if answer[1] == "":
            return answer[0]
        return False

    @lru_cache
    def _matches(self, input: str, index: int) -> bool:
        # print(input, index, self.book[index])
        if stack_size2a() > 200:
            return (True, "")

        if input == "":
            return (False, "")

        sub_rule = self.book[index]
        if isinstance(sub_rule, Value):
            return (input[0] == sub_rule.value, input[1:])

        for option in sub_rule.options:
            line = input
            valids = []
            for (_match_index, sub_index) in enumerate(option.indexes):
                (a, line) = self._matches(line, sub_index)
                valids.append((a, line))
            # print(line, valids)

            if all((x[0] for x in valids)):
                return valids[-1]
            else:
                continue

        return (False, input)


def parse_rules(text_lines):
    return RuleBook([parse_rule(line) for line in text_lines])


def parse_rule(text_line):
    [index, rest] = text_line.split(":")
    index = int(index)
    rest = rest.strip()
    if '"' in rest:
        rest = rest.strip('"')
        return Rule(index, Value(rest))

    groups = [x.strip() for x in rest.split("|")]
    rules = [Option([int(x) for x in y.split()]) for y in groups]
    return Rule(index, SubRule(rules))


def main():
    with open("data.txt") as f:
        [rules, messages] = f.read().split("\n\n")
        rules = rules.splitlines()
        rule_book = parse_rules(rules)
        # print(rule_book.matches("aabbbb"))

        counter = 0
        for message in messages.splitlines():
            print("hey")
            if rule_book.matches(message):
                counter += 1

        print(counter)


if __name__ == "__main__":
    main()
