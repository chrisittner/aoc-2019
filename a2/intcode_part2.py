from intcode import IntcodeProgram

if __name__ == "__main__":
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [1, 0, 0, 3]

        target_output = 19690720

        for noun in range(100):
            for verb in range(100):
                program[1] = noun
                program[2] = verb

                machine = IntcodeProgram(program[:])
                machine.run()

                if machine.program[0] == target_output:
                    print(noun, verb)
                    print(100 * noun + verb)
