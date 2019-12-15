from typing import Tuple
from collections import defaultdict
from time import sleep
from intcode import IntcodeMachine


def sign(x):
    if x == 0:
        return 0

    return -1 if x < 0 else 1


class ArcadeGame:
    def __init__(self, program, screen_size: Tuple[int, int] = (44, 20)):
        self.machine = IntcodeMachine(program)
        self.screen = defaultdict(lambda: 0)
        self.score = 0
        self.screen_size = screen_size

    def draw_screen(self):
        assert not self.machine.output
        self.machine.run()
        while len(self.machine.output) >= 3:
            self.draw_tile()
        assert not self.machine.output

    def draw_tile(self):
        assert len(self.machine.output) >= 3
        x = self.machine.output.pop(0)
        y = self.machine.output.pop(0)

        if (x, y) == (-1, 0):
            score = self.machine.output.pop(0)
            self.score = score
        else:
            tile_type = self.machine.output.pop(0)
            self.screen[(x, y)] = tile_type

    def count_block_tiles(self):
        return list(self.screen.values()).count(2)

    def print_screen(self):
        size_x, size_y = self.screen_size
        for y in range(size_y):
            line = []
            for x in range(size_x):
                line += self.tile_type_to_char(self.screen[(x, y)])
            print("".join(line))

    def play_step(self):
        self.draw_screen()
        self.print_screen()

        joystick_input = input(f"Score: {self.score}. Move with asd..")
        # print(f"Score: {self.score}. Move with asd..")
        # joystick_input = sys.stdin.read(1)

        joystick_commands = {"s": 0, "a": -1, "d": 1}
        assert joystick_input in joystick_commands.keys()

        self.machine.input.append(joystick_commands[joystick_input])

    def play(self):
        while not self.machine.halted:
            self.play_step()

        print(self.score)

    def auto_step(self):
        self.draw_screen()
        for coord, tile in self.screen.items():
            if tile == 3:
                bar_x = coord[0]
            if tile == 4:
                ball_x = coord[0]

        bar_should_move = sign(ball_x - bar_x)

        self.machine.input.append(bar_should_move)

    def auto_play(self):
        while not self.machine.halted:
            self.auto_step()
            self.print_screen()
            sleep(0.05)
            print(f"Score: {self.score}")

        print(f"Score: {self.score}")

    def auto_play_silent(self):
        while not self.machine.halted:
            self.auto_step()
        print(self.score)

    @staticmethod
    def tile_type_to_char(tile: int):
        return [".", "#", "x", "_", "o"][tile]


if __name__ == "__main__":
    with open("input_a13") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:6] == [1, 380, 379, 385, 1008, 2399]

        program[0] = 2  # insert quarter

        game = ArcadeGame(program)
        game.auto_play()

        # assert game.count_block_tiles() == 200
