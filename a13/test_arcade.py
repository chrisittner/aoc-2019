from .arcade import ArcadeGame


def test_part1():
    with open("input_a13") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:6] == [1, 380, 379, 385, 1008, 2399]

        game = ArcadeGame(program)
        game.draw_screen()

        assert game.count_block_tiles() == 200


def test_part2():
    with open("input_a13") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:6] == [1, 380, 379, 385, 1008, 2399]

        program[0] = 2  # insert quarter

        game = ArcadeGame(program)
        game.auto_play_silent()

        assert game.score == 9803
