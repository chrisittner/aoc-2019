from itertools import permutations
from intcode import IntcodeMachine


def thruster_power(program, phase_setting_sequence):
    amp_input = 0

    for ii in range(5):
        amp = IntcodeMachine(program[:], input=[phase_setting_sequence[ii], amp_input])
        amp.run()
        amp_input = amp.output[0]

    return amp_input


def max_thruster_power(program):
    max_power = thruster_power(program, [0, 1, 2, 3, 4])
    for phase_setting_sequence in permutations(list(range(5))):
        power = thruster_power(program, phase_setting_sequence)
        max_power = max(max_power, power)

    return max_power


def thruster_power_part2(program, phase_setting_sequence):
    amps = [
        IntcodeMachine(program[:], input=[phase_setting_sequence[ii]])
        for ii in range(5)
    ]

    amp_input = 0
    while not any([amp.halted for amp in amps]):
        for amp in amps:
            amp.input.append(amp_input)
            amp.run()
            amp_input = amp.output.pop()

    return amp_input


def max_thruster_power_part2(program):
    max_power = thruster_power_part2(program, [5, 6, 7, 8, 9])
    for phase_setting_sequence in permutations(list(range(5, 10))):
        power = thruster_power_part2(program, phase_setting_sequence)
        max_power = max(max_power, power)

    return max_power


if __name__ == "__main__":
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]

        assert max_thruster_power(program) == 79723

        print(max_thruster_power_part2(program))
