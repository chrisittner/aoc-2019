class WaitingForInput(Exception):
    pass


class IntcodeMachine:
    def __init__(self, program: list, input: list = None, instruction_pointer: int = 0):
        self.memory = program[:]
        self.input = input if input else []
        self.output = []

        self.instruction_pointer = instruction_pointer
        self.relative_base = 0
        self.halted = False

    @staticmethod
    def number_of_parameters(instruction):
        return {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}[
            instruction
        ]

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

    def get_value(self, param, param_mode) -> int:
        if param_mode == 0:
            value = self._read_from_memory(param)
        elif param_mode == 1:
            value = param
        elif param_mode == 2:
            value = self._read_from_memory(self.relative_base + param)
        else:
            raise ValueError("Bad Parameter Mode")

        return value

    def _read_from_memory(self, addr) -> int:
        if len(self.memory) <= addr:
            self.memory.extend([0] * (addr + 1 - len(self.memory)))

        return self.memory[addr]

    def _write_to_memory(self, addr_param, mode, value):
        assert mode in (0, 2)
        addr = addr_param if mode == 0 else self.relative_base + addr_param

        if len(self.memory) <= addr:
            self.memory.extend([0] * (addr + 1 - len(self.memory)))

        self.memory[addr] = value

    def run_instruction(self):
        instruction, params, param_modes = self.read_instruction()
        self.instruction_pointer += 1 + len(params)

        if instruction in (1, 2, 7, 8):
            val1 = self.get_value(params[0], param_modes[0])
            val2 = self.get_value(params[1], param_modes[1])

            if instruction == 1:
                value_to_write = val1 + val2
            elif instruction == 2:
                value_to_write = val1 * val2
            elif instruction == 7:
                value_to_write = int(val1 < val2)
            elif instruction == 8:
                value_to_write = int(val1 == val2)
            else:
                raise ValueError("Invalid opcode")

            self._write_to_memory(params[2], param_modes[2], value_to_write)

        elif instruction == 3:
            if not self.input:
                self.instruction_pointer -= 1 + len(params)
                raise WaitingForInput()
            self._write_to_memory(params[0], param_modes[0], self.input.pop(0))

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

        elif instruction == 9:
            relative_base_offset = self.get_value(params[0], param_modes[0])
            self.relative_base += relative_base_offset

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
    with open("input_a9") as fp:
        source_code = fp.read()
        program = [int(instr) for instr in source_code.split(",")]
        assert program[:5] == [1102, 34463338, 34463338, 63, 1007]

        machine = IntcodeMachine(program, input=[2])
        machine.run()

        print(machine.output)
