from enum import Enum
from dataclasses import dataclass
from typing import Union, Any
from pprint import pprint


class Operator(Enum):
    Add = "+"
    Mul = "*"

    def apply(self, lhs, rhs):
        if self == Operator.Add:
            return lhs + rhs

        if self == Operator.Mul:
            return lhs * rhs


@dataclass
class Expr:
    lhs: Union[int, "Expr"]
    rhs: Union[int, "Expr"]
    operator: "Operator"

    def __str__(self):
        return f"({self.lhs} {self.operator.value} {self.rhs})"

    def eval(self):
        if isinstance(self.lhs, Expr):
            lhs = self.lhs.eval()
        else:
            lhs = self.lhs

        if isinstance(self.rhs, Expr):
            rhs = self.rhs.eval()
        else:
            rhs = self.rhs

        return self.operator.apply(lhs, rhs)

    @staticmethod
    def parse(line):
        (_, acc) = lexer(line, Accumulator([]))
        expr = treeify(acc.state)
        return expr


@dataclass
class Value:
    value: Any

    def __str__(self):
        return str(self.value)

    def __mul__(self, other):
        return Value(self.value * other.value)

    def __add__(self, other):
        return Value(self.value + other.value)


@dataclass
class Accumulator:
    state: list
    index: int = 0
    depth: int = 0

    def push(self, item):
        self.state.append((self.index, self.depth, item))
        self.index += 1

    def inc_depth(self):
        self.depth += 1


def lexer(line: str, acc: Accumulator):
    if len(line) == 0:
        return (line, acc)

    char = line[0]
    rest = line[1:]

    if char == " ":
        return lexer(rest, acc)
    if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        acc.push(Value(int(char)))
        return lexer(rest, acc)
    if char == Operator.Add.value:
        acc.push(Operator.Add)
        return lexer(rest, acc)
    if char == Operator.Mul.value:
        acc.push(Operator.Mul)
        return lexer(rest, acc)
    if char == "(":
        acc.inc_depth()
        (rest, other_acc) = lexer(rest, Accumulator([]))
        acc.push(other_acc)
        return lexer(rest, acc)
    if char == ")":
        return (rest, acc)

    raise Exception("invalid expression")


# # part one sollution
# def apply_brackets(prev, line):
#     if line == []:
#         return prev

#     if prev is None:
#         return apply_brackets(Expr(line[0], line[2], line[1]), line[3:])
#     else:
#         return apply_brackets(Expr(prev, line[1], line[0]), line[2:])


def apply_brackets(line):
    if len(line) == 1 and isinstance(line[0], Expr):
        return line[0]

    if len(line) >= 5:

        if line[3] == Operator.Add:
            line[2] = Expr(line[2], line[4], line[3])
            del line[4]
            del line[3]

            return apply_brackets(line)

        line[0] = Expr(line[0], line[2], line[1])

        del line[2]
        del line[1]

        return apply_brackets(line)
    if len(line) == 3:
        line[0] = Expr(line[0], line[2], line[1])
        del line[2]
        del line[1]
        return apply_brackets(line)

    raise Exception("Invalid expression")


def index(list, item):
    try:
        return list.index(item)
    except ValueError:
        return None


def treeify(state):
    tmp = []
    for (_, _, item) in state:
        if isinstance(item, Accumulator):
            tmp.append(treeify(item.state))
        else:
            tmp.append(item)

    # return apply_brackets(None, tmp)
    return apply_brackets(tmp)


# # has python (the actual) rules already baked in
# def parse(line):
#     tree = ast.parse(line)
#     print(cast(tree.body[0].value))
#
# def cast(val):
#     if isinstance(val, ast.Mult):
#         return Operator.Mul
#     if isinstance(val, ast.Add):
#         return Operator.Add
#     if isinstance(val, ast.Constant):
#         return val.value
#     if isinstance(val, ast.BinOp):
#         return Expr(cast(val.left), cast(val.right), cast(val.op))


def main():
    with open("data.txt") as f:
        data = f.read().splitlines()

        answers = []
        for line in data:
            answers.append(Expr.parse(line).eval().value)

        print(sum(answers))


if __name__ == "__main__":
    main()
