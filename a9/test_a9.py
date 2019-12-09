from .intcode import IntcodeMachine


def test_quine():
    quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    machine = IntcodeMachine(quine)
    machine.run()

    assert machine.output == quine


def test_large_num():
    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    machine = IntcodeMachine(program)
    machine.run()

    assert len(machine.output) == 1
    assert len(str(machine.output[0])) == 16


def test_large_num2():
    program = [104, 1125899906842624, 99]
    machine = IntcodeMachine(program)
    machine.run()

    assert machine.output == [1125899906842624]


def test_write_in_rel_mode():
    pass


def test_a9_part1():
    with open("input_a9") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:5] == [1102, 34463338, 34463338, 63, 1007]

        machine = IntcodeMachine(program, input=[1])
        machine.run()

        assert machine.output == [3429606717]


def test_a9_part2():
    with open("input_a9") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:5] == [1102, 34463338, 34463338, 63, 1007]

        machine = IntcodeMachine(program, input=[2])
        machine.run()

        assert machine.output == [33679]
