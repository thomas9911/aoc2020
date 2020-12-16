from dataclasses import dataclass
from pprint import pprint
from collections import defaultdict


@dataclass
class Rule:
    name: str
    ranges: ["range"]

    def valid(self, number):
        return any([(number in r) for r in self.ranges])

    def all_valid(self, numbers):
        return all(self.valid(x) for x in numbers)

    def name_startswith(self, string):
        return self.name.startswith(string)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class Ticket:
    numbers: [int]

    def all_valid(self, rule: Rule):
        return all([rule.valid(x) for x in self.numbers])

    def any_valid(self, rule: Rule):
        return any([rule.valid(x) for x in self.numbers])

    def get_invalid_numbers(self, rule: Rule):
        return [x for x in self.numbers if not rule.valid(x)]

    def valid(self, rules: [Rule]):
        valid_dict = {}
        for number in self.numbers:
            valid_dict[number] = any((r.valid(number) for r in rules))
        return all(valid_dict.values())

    def map_values(self, mapping):
        new_mapping = {}
        for (rule, v) in mapping.items():
            new_mapping[rule] = self.numbers[v]

        return new_mapping


class Analyzer:
    def __init__(self, rules):
        self.rules = rules
        self._tickets = []

    @property
    def tickets(self):
        return self._tickets

    @tickets.setter
    def tickets(self, value):
        if isinstance(value, list):
            self._tickets = value
        else:
            raise TypeError

    def get_invalid_numbers(self):
        invalids = []
        for ticket in self.tickets:
            invalid_numbers = ticket.numbers
            for rule in self.rules:
                invalid_numbers = Ticket(invalid_numbers).get_invalid_numbers(rule)
            invalids.extend(invalid_numbers)

        return invalids

    def trim_invalid_tickets(self):
        valids_tickets = []
        for ticket in self.tickets:
            if ticket.valid(self.rules):
                valids_tickets.append(ticket)

        self.tickets = valids_tickets

    def _find_valid_column(self):
        valid_rule_map = defaultdict(list)
        for index in range(0, len(self.rules)):
            for rule in self.rules:
                if rule.all_valid([ticket.numbers[index] for ticket in self.tickets]):
                    valid_rule_map[index].append(rule)

        return valid_rule_map

    def _find_rule_mapping(self, valid_rule_map):
        mapping = {}
        found_columns = []

        while len(mapping) != len(valid_rule_map):
            for (a, rules) in valid_rule_map.items():
                if a in mapping:
                    continue

                rules = [
                    x for x in filter(lambda x: x.name not in found_columns, rules)
                ]
                if len(rules) == 1:
                    mapping[a] = rules[0]
                    found_columns.append(rules[0].name)

        return mapping

    def align_rules(self):
        valid_rule_map = self._find_valid_column()
        mapping = self._find_rule_mapping(valid_rule_map)
        # print(mapping)
        lookup = {v: k for (k, v) in mapping.items()}
        return lookup


def parse_header(text):
    lines = text.splitlines()
    rules = []
    for line in lines:
        (name, ranges_text) = line.split(":")
        ranges = []
        for r in ranges_text.strip().split(" or "):
            [from_, to] = [int(x) for x in r.strip().split("-")]
            # ranges in python are exclusive ranges, but we need inclusive ranges
            ranges.append(range(from_, to + 1))

        rules.append(Rule(name, ranges))
    return rules


def parse_your_ticket(text):
    return Ticket([int(x) for x in text.splitlines()[1].split(",")])


def parse_other_tickets(text):
    tickets_text = text.splitlines()[1:]
    tickets = []
    for ticket_text in tickets_text:
        tickets.append(Ticket([int(x) for x in ticket_text.split(",")]))

    return tickets


def solution_b(your_ticket, lookup):
    mapping = your_ticket.map_values(lookup)

    sol = 1
    for (rule, val) in mapping.items():
        if rule.name_startswith("departure"):
            sol *= val

    return sol


def main():
    with open("data.txt") as f:
        data = f.read().split("\n\n")
        rules = parse_header(data[0])
        your_ticket = parse_your_ticket(data[1])
        other_tickets = parse_other_tickets(data[2])

        a = Analyzer(rules)
        a.tickets = other_tickets
        a.trim_invalid_tickets()

        lookup = a.align_rules()

        print(solution_b(your_ticket, lookup))


if __name__ == "__main__":
    main()
