class IntcodeProgram:
    def __init__(self, program: list):
        self.program = program  # memory

    def run(self, instruction_pointer: int = 0):
        if len(self.program) < instruction_pointer:
            raise ValueError("Unexpected EOF")

        elif self.program[instruction_pointer] in (1, 2):
            if len(self.program) < (instruction_pointer + 3):
                raise ValueError("Invalid syntax: missing parameter")

            source_addr1, source_addr2, dest_addr = self.program[
                (instruction_pointer + 1) : (instruction_pointer + 4)
            ]

            if self.program[instruction_pointer] == 1:
                self.program[dest_addr] = (
                    self.program[source_addr1] + self.program[source_addr2]
                )
            elif self.program[instruction_pointer] == 2:
                self.program[dest_addr] = (
                    self.program[source_addr1] * self.program[source_addr2]
                )

            self.run(instruction_pointer + 4)

        elif self.program[instruction_pointer] == 99:
            pass

        else:
            raise ValueError("Invalid opcode")

    @staticmethod
    def pretty_print(program: list) -> str:
        if not program:
            return ""
        elif program[0] == 99:
            return "\t".join([str(i) for i in program])
        else:
            return (
                "\t".join([str(i) for i in program[0:4]])
                + "\n"
                + IntcodeProgram.pretty_print(program[4:])
            )

    def __repr__(self) -> str:
        return self.pretty_print(self.program)


if __name__ == "__main__":
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [1, 0, 0, 3]

        # restore failed state
        program[1] = 12
        program[2] = 2

        machine = IntcodeProgram(program)
        machine.run()

        print(machine)

