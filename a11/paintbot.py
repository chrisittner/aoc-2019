from collections import defaultdict
from enum import Enum
from intcode import IntcodeMachine


class Direction(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    def next(self):
        members = list(self.__class__)
        index = (members.index(self) + 1) % len(members)
        return members[index]

    def prev(self):
        members = list(self.__class__)
        index = (members.index(self) - 1) % len(members)
        return members[index]

    turn_left = prev
    turn_right = next


class PaintBot:
    def __init__(self, program, start_location_color="#"):
        self.machine = IntcodeMachine(program)
        self.grid = defaultdict(lambda: ".")
        self.location = (0, 0)
        self.grid[self.location] = start_location_color
        self.direction = Direction.UP

        self.painted_fields = []

    def run_step(self):
        current_color = self.grid[self.location]

        assert not self.machine.input and not self.machine.output
        self.machine.input.append(0 if current_color == "." else 1)
        self.machine.run()

        assert len(self.machine.output) == 2
        new_color = self.machine.output.pop(0)
        assert new_color in (0, 1)
        self.grid[self.location] = "." if new_color == 0 else "#"

        if self.location not in self.painted_fields:
            self.painted_fields.append(self.location)

        direction_change = self.machine.output.pop(0)
        assert direction_change in (0, 1)
        self.direction = (
            self.direction.turn_left()
            if direction_change == 0
            else self.direction.turn_right()
        )

        self.location = (
            self.location[0] + self.direction.value[0],
            self.location[1] + self.direction.value[1],
        )

    def run(self):
        while not self.machine.halted:
            self.run_step()

    def print_grid(self):
        x_min = min([x for x, y in self.painted_fields])
        x_max = max([x for x, y in self.painted_fields])
        y_min = min([y for x, y in self.painted_fields])
        y_max = max([y for x, y in self.painted_fields])

        for y in range(y_max, y_min - 1, -1):
            row = []
            for x in range(x_min, x_max + 1):
                row.append(self.grid[x, y])
            print("".join(row))


if __name__ == "__main__":
    with open("input_a11") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:6] == [3, 8, 1005, 8, 339, 1106]

        paintbot = PaintBot(program)
        paintbot.run()

        assert paintbot.machine.halted
        print(len(paintbot.painted_fields))
        # paintbot.print_grid()  # LEPCPLGZ
        # .  # ....####.###...##..###..#.....##..####...
        # .  # ....#....#..#.#..#.#..#.#....#..#....#...
        # .  # ....###..#..#.#....#..#.#....#......#....
        # .  # ....#....###..#....###..#....#.##..#.....
        # .  # ....#....#....#..#.#....#....#..#.#......
        # .  ####.####.#.....##..#....####..###.####...
