import pytest
from .intcode import IntcodeMachine


@pytest.mark.parametrize(
    "program, end_state",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
    ],
)
def test_intcode_program(program, end_state):
    machine = IntcodeMachine(program)
    machine.run()
    assert machine.memory == end_state


def test_a2():
    with open("input_a2") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [1, 0, 0, 3]

        # restore failed state
        program[1] = 12
        program[2] = 2

        machine = IntcodeMachine(program)
        machine.run()

        assert machine.memory[0] == 3101844


def test_io():
    program = [3, 0, 4, 0, 99]
    machine = IntcodeMachine(program, input=[42, 43])
    machine.run()
    assert machine.memory == program
    assert machine.input == [43]
    assert machine.output == [42]


@pytest.mark.parametrize(
    "program,end_state",
    [
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99]),
    ],
)
def test_value_mode(program, end_state):
    machine = IntcodeMachine(program)
    machine.run()
    assert machine.memory == end_state


def test_a5_part1():
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [3, 225, 1, 225]

        machine = IntcodeMachine(program, input=[1])
        machine.run()

        assert machine.output == [0, 0, 0, 0, 0, 0, 0, 0, 0, 11193703]


@pytest.mark.parametrize(
    "program",
    [([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]), ([3, 3, 1108, -1, 8, 3, 4, 3, 99])],
)
def test_78_is_eq_8(program):
    machine = IntcodeMachine(program, input=[7])
    machine.run()
    assert machine.output == [0]

    machine = IntcodeMachine(program, input=[8])
    machine.run()
    assert machine.output == [1]

    machine = IntcodeMachine(program, input=[9])
    machine.run()
    assert machine.output == [0]


@pytest.mark.parametrize(
    "program",
    [([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]), ([3, 3, 1107, -1, 8, 3, 4, 3, 99])],
)
def test_78_is_lt_8(program):
    machine = IntcodeMachine(program[:], input=[8])
    machine.run()
    assert machine.output == [0]

    machine = IntcodeMachine(program[:], input=[7])
    machine.run()
    assert machine.output == [1]


@pytest.mark.parametrize(
    "program",
    [
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]),
    ],
)
def test_jump(program):
    machine = IntcodeMachine(program[:], input=[0])
    machine.run()
    assert machine.output == [0]

    machine = IntcodeMachine(program[:], input=[1])
    machine.run()
    assert machine.output == [1]

    machine = IntcodeMachine(program[:], input=[5])
    machine.run()
    assert machine.output == [1]


def test_jump2():
    program = [
        3,
        21,
        1008,
        21,
        8,
        20,
        1005,
        20,
        22,
        107,
        8,
        21,
        20,
        1006,
        20,
        31,
        1106,
        0,
        36,
        98,
        0,
        0,
        1002,
        21,
        125,
        20,
        4,
        20,
        1105,
        1,
        46,
        104,
        999,
        1105,
        1,
        46,
        1101,
        1000,
        1,
        20,
        4,
        20,
        1105,
        1,
        46,
        98,
        99,
    ]
    machine = IntcodeMachine(program[:], input=[5])
    machine.run()
    assert machine.output == [999]

    machine = IntcodeMachine(program[:], input=[8])
    machine.run()
    assert machine.output == [1000]

    machine = IntcodeMachine(program[:], input=[123])
    machine.run()
    assert machine.output == [1001]


def test_a5_part2():
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [3, 225, 1, 225]

        machine = IntcodeMachine(program, input=[5])
        machine.run()

        assert machine.output == [12410607]
