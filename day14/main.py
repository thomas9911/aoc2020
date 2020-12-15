from enum import Enum
import ast
import itertools

MASK_SIZE = 36


class Memory(dict):
    def __init__(self):
        self.currect_mask = None
        super().__init__()

    def run(self, instruction):
        if isinstance(instruction, Mask):
            self.currect_mask = instruction
            return

        if isinstance(instruction, Set):
            # self._set_instruction_a(instruction)
            self._set_instruction_b(instruction)
            return

        raise Exception("Invalid instruction")

    def _set_instruction_a(self, instruction):
        binary = apply_mask_a(self.currect_mask.mask, instruction.expand_value())
        new_value = int(binary, 2)
        self[instruction.address] = new_value

    def _set_instruction_b(self, instruction):
        new_mask = apply_mask_b(self.currect_mask.mask, instruction.expand_address())
        for address in new_mask.expand_mask():
            new_address = int(address.mask_binary(), 2)
            self[new_address] = instruction.value


class MaskValue(Enum):
    Zero = "0"
    One = "1"
    Keep = "X"


class Instruction:
    pass


class Mask(Instruction):
    def __init__(self, mask):
        self.mask = self._transform_mask(mask)

    @staticmethod
    def raw(mask_list):
        mask = Mask("")
        mask.mask = mask_list
        return mask

    def expand_mask(self):
        counter = self.mask.count(MaskValue.Keep)
        if counter == 0:
            return [self.mask]

        result = {x: [] for x in range(2 ** counter)}

        what_x = 0
        for value in self.mask:
            if value != MaskValue.Keep:
                for key in result.keys():
                    result[key].append(value)

            if value == MaskValue.Keep:
                for (index, subs) in enumerate(
                    itertools.product([MaskValue.Zero, MaskValue.One], repeat=counter)
                ):
                    result[index].append(subs[what_x])

                what_x += 1

        return [Mask(mask_list) for mask_list in result.values()]

    def mask_binary(self):
        return "".join([mask_value.value for mask_value in self.mask])

    @staticmethod
    def _transform_mask(mask):
        return [MaskValue(x) for x in mask]

    def __repr__(self):
        return f"Mask(mask={self.mask})"


class Set(Instruction):
    def __init__(self, address, value):
        self.address = address
        self.value = value

    def expand_address(self):
        return expand_integer(self.address)

    def expand_value(self):
        return expand_integer(self.value)

    def __repr__(self):
        return f"Set(address={self.address}, value={self.value})"


def parse_line(line):
    # instructions are valid python-like statements :+1:
    # only the mask 1XX1XX is not valid python :(

    if line.startswith("mask"):
        return Mask(line.replace("mask = ", ""))

    if line.startswith("mem"):
        tree = ast.parse(line)
        assign = tree.body[0]

        _mem = assign.targets[0].value.id
        address = assign.targets[0].slice.value.value
        value = assign.value.value
        return Set(address, value)

    raise Exception("invalid line")


def apply_mask_a(mask, binary_str):
    binary_list = []
    for (a, b) in zip(mask, binary_str):
        if a == MaskValue.Keep:
            binary_list.append(b)
            continue

        if a == MaskValue.One:
            binary_list.append("1")
            continue

        if a == MaskValue.Zero:
            binary_list.append("0")
            continue

    binary = "".join(binary_list)
    return binary


def apply_mask_b(mask, binary_str):
    mask_list = []
    for (a, b) in zip(mask, binary_str):
        if a == MaskValue.Keep:
            mask_list.append(MaskValue.Keep)
            continue

        if a == MaskValue.One:
            mask_list.append(MaskValue.One)
            continue

        if a == MaskValue.Zero:
            mask_list.append(MaskValue(b))
            continue

    return Mask.raw(mask_list)


def expand_integer(integer):
    return f"{integer:0{MASK_SIZE}b}"


def main():
    with open("data.txt") as f:
        data = f.read().splitlines()
        instructions = [parse_line(x) for x in data]

        m = Memory()

        for i in instructions:
            m.run(i)

        print(sum(m.values()))


if __name__ == "__main__":
    main()
