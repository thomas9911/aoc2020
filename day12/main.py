from enum import Enum
import math


def degree_to_rad(degree):
    # 90 = 1/2 * math.pi()
    # 180 = math.pi()
    return degree / 180 * math.pi


class Action(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


class Instruction:
    def __init__(self, action: Action, value: int):
        self.action = action
        self.value = value

    @staticmethod
    def parse(text):
        action = Action(text[0])
        value = int(text[1:])
        return Instruction(action, value)

    def __repr__(self):
        return f"Instruction(action={self.action}, value={self.value})"


# class Ferry:
#     def __init__(self):
#         # use math axis (instead of graphs axis)
#         self.x = 0
#         self.y = 0
#         self.direction = 0 # 0 is east

#     def run(self, instruction: Instruction):
#         if instruction.action == Action.NORTH:
#             self.y += instruction.value
#             return
#         if instruction.action == Action.SOUTH:
#             self.y -= instruction.value
#             return
#         if instruction.action == Action.EAST:
#             self.x += instruction.value
#             return
#         if instruction.action == Action.WEST:
#             self.x -= instruction.value
#             return

#         if instruction.action == Action.LEFT:
#             self.direction += instruction.value
#             return
#         if instruction.action == Action.RIGHT:
#             self.direction -= instruction.value
#             return
#         if instruction.action == Action.FORWARD:
#             radians = degree_to_rad(self.direction)
#             self.y += instruction.value*math.sin(radians)
#             self.x += instruction.value*math.cos(radians)
#             return

#         raise "Invalid Instruction"


class Waypoint:
    def __init__(self):
        self.x = 10
        self.y = 1

    def update(self, instruction: Instruction):
        if instruction.action == Action.NORTH:
            self.y += instruction.value
            return
        if instruction.action == Action.SOUTH:
            self.y -= instruction.value
            return
        if instruction.action == Action.EAST:
            self.x += instruction.value
            return
        if instruction.action == Action.WEST:
            self.x -= instruction.value
            return

        if instruction.action == Action.FORWARD:
            return

        return self._rotate_90(instruction)

    def _rotate_90(self, instruction):
        # if instruction.action == Action.LEFT:
        #     radians = degree_to_rad(instruction.value)
        #     x = self.x
        #     y = self.y
        #     self.x = x*math.cos(radians) - y*math.sin(radians)
        #     self.y = x*math.sin(radians) - y*math.cos(radians)
        #     return
        # if instruction.action == Action.RIGHT:
        #     radians = -degree_to_rad(instruction.value)
        #     x = self.x
        #     y = self.y
        #     self.x = x*math.cos(radians) - y*math.sin(radians)
        #     self.y = x*math.sin(radians) - y*math.cos(radians)
        #     return

        if instruction.value < 0:
            raise Exception("noi")
        if instruction.value % 90 != 0:
            raise Exception("noi")
        value = instruction.value // 90

        x = self.x
        y = self.y

        if value == 1:
            if instruction.action == Action.LEFT:
                self.x = -y
                self.y = x
                return
            if instruction.action == Action.RIGHT:
                self.x = y
                self.y = -x
                return
        if value == 2:
            self.x = -x
            self.y = -y
            return
        if value == 3:
            if instruction.action == Action.LEFT:
                self.x = y
                self.y = -x
                return
            if instruction.action == Action.RIGHT:
                self.x = -y
                self.y = x
                return
        if value == 4:
            return


class Ferry:
    def __init__(self):
        # use math axis (instead of graphs axis)
        self.x = 0
        self.y = 0
        self.waypoint = Waypoint()
        self.direction = 0  # 0 is east

    def run_a(self, instruction: Instruction):
        if instruction.action == Action.NORTH:
            self.y += instruction.value
            return
        if instruction.action == Action.SOUTH:
            self.y -= instruction.value
            return
        if instruction.action == Action.EAST:
            self.x += instruction.value
            return
        if instruction.action == Action.WEST:
            self.x -= instruction.value
            return

        if instruction.action == Action.LEFT:
            self.direction += instruction.value
            return
        if instruction.action == Action.RIGHT:
            self.direction -= instruction.value
            return
        if instruction.action == Action.FORWARD:
            radians = degree_to_rad(self.direction)
            self.y += instruction.value * math.sin(radians)
            self.x += instruction.value * math.cos(radians)
            return

    def run_b(self, instruction: Instruction):

        if instruction.action == Action.FORWARD:
            return self.move(instruction.value)
        else:
            return self.waypoint.update(instruction)

        raise "Invalid Instruction"

    def move(self, value):
        self.x += value * self.waypoint.x
        self.y += value * self.waypoint.y

    @property
    def distance(self):
        return round(abs(self.x) + abs(self.y))


def main():
    with open("data.txt") as f:
        data = f.read().splitlines()
        instructions = [Instruction.parse(x) for x in data]

        f = Ferry()
        for instruction in instructions:
            f.run_a(instruction)
            # f.run_b(instruction)

        print(f.distance)


if __name__ == "__main__":
    main()
