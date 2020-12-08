from pprint import pprint

PLACEHOLDER = "abcdefg"


class Console:
    def __init__(self):
        self.clear()

    def clear(self):
        self.acc = 0
        self.line = 0
        self.counter = 0
        self.last_command = None

    def instruction(self, line):
        [command, counter] = line.split(" ")

        if command == "nop":
            self.line += 1
            self.counter += 1
            self.last_command = command
            return

        if command == "acc":
            self.acc += int(counter)
            self.line += 1
            self.counter += 1
            self.last_command = command
            return

        if command == "jmp":
            self.line += int(counter)
            self.counter += 1
            self.last_command = command
            return

        raise "Invalid Instruction"

    """
    Return True on successfull execution. Returns False on Error (infinite loop)
    """

    def run(self, program):
        lines_ran = []

        while len(program) > self.line:
            self.instruction(program[self.line])
            lines_ran.append(self.line)
            if len(lines_ran) != len(set(lines_ran)):
                return False

        return True


def _fixable_commands(program):
    commands = ["jmp", "nop"]

    new_program = []
    for (number, line) in enumerate(program):
        xd = False
        for command in commands:
            xd |= line.startswith(command)

        new_program.append((number, xd))

    return new_program


def fix_line(line):
    return (
        line.replace("nop", PLACEHOLDER)
        .replace("jmp", "nop")
        .replace(PLACEHOLDER, "jmp")
    )


def fix(program):
    console = Console()

    labeled_program = _fixable_commands(program)
    index = 0

    fixed = False
    while not fixed:
        (line_number, fixable) = labeled_program[index]
        if not fixable:
            index += 1
            continue

        fixed_program = program.copy()
        fixed_program[line_number] = fix_line(fixed_program[line_number])

        console.clear()
        fixed = console.run(fixed_program)
        index += 1

    return fixed_program


with open("data.txt") as f:
    data = f.read()

    program = data.splitlines()

    fixed_program = fix(program)

    console = Console()
    console.run(fixed_program)
    print(console.acc)
