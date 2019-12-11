from .paintbot import PaintBot


def test_part1():
    with open("input_a11") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:6] == [3, 8, 1005, 8, 339, 1106]

        paintbot = PaintBot(program, start_location_color=".")
        paintbot.run()
        assert len(paintbot.painted_fields) == 2883
