class WaitingForInput(Exception):
    pass


class IntcodeMachine:
    def __init__(self, program: list, input: list = None, instruction_pointer: int = 0):
        self.memory = program
        self.input = input if input else []
        self.output = []

        self.instruction_pointer = instruction_pointer
        self.halted = False

    @staticmethod
    def number_of_parameters(instruction):
        return {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}[instruction]

    def read_instruction(self) -> (int, list):
        assert not self.halted

        if len(self.memory) < self.instruction_pointer:
            raise ValueError("Unexpected EOF")

        intcode = str(self.memory[self.instruction_pointer])
        instruction = int(intcode[-2:])
        num_params = self.number_of_parameters(instruction)

        parameter_modes = list(reversed([int(mode) for mode in intcode[:-2]]))
        parameter_modes += [0] * (num_params - len(parameter_modes))

        param_addr = self.instruction_pointer + 1

        if len(self.memory) < (self.instruction_pointer + num_params):
            raise ValueError("Invalid syntax: missing parameter")

        parameters = self.memory[param_addr : param_addr + num_params]

        return instruction, parameters, parameter_modes

    def get_value(self, param, param_mode):
        return param if param_mode else self.memory[param]

    def run_instruction(self):
        instruction, params, param_modes = self.read_instruction()
        self.instruction_pointer += 1 + len(params)

        if instruction in (1, 2, 7, 8):
            val1 = self.get_value(params[0], param_modes[0])
            val2 = self.get_value(params[1], param_modes[1])
            assert not param_modes[2]

            if instruction == 1:
                self.memory[params[2]] = val1 + val2
            elif instruction == 2:
                self.memory[params[2]] = val1 * val2
            elif instruction == 7:
                self.memory[params[2]] = int(val1 < val2)
            elif instruction == 8:
                self.memory[params[2]] = int(val1 == val2)

        elif instruction == 3:
            assert not param_modes[0]
            if not self.input:
                self.instruction_pointer -= 1 + len(params)
                raise WaitingForInput()
            self.memory[params[0]] = self.input.pop(0)

        elif instruction == 4:
            self.output.append(self.get_value(params[0], param_modes[0]))

        elif instruction == 5:
            val = self.get_value(params[0], param_modes[0])
            ptr_val = self.get_value(params[1], param_modes[1])
            if val:
                self.instruction_pointer = ptr_val

        elif instruction == 6:
            val = self.get_value(params[0], param_modes[0])
            ptr_val = self.get_value(params[1], param_modes[1])
            if not val:
                self.instruction_pointer = ptr_val

        elif instruction == 99:
            self.halted = True

        else:
            raise ValueError("Invalid opcode")

    def run(self):
        while not self.halted:
            try:
                self.run_instruction()
            except WaitingForInput:
                break

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
                + IntcodeMachine.pretty_print(program[4:])
            )

    def __repr__(self) -> str:
        return self.pretty_print(self.memory)


if __name__ == "__main__":
    with open("input") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:4] == [3, 225, 1, 225]

        machine = IntcodeMachine(program, input=[5])
        machine.run()

        print(machine.output)
