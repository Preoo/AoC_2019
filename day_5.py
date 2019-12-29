from enum import IntEnum
from collections import deque

class OpCode(IntEnum):
    ADD = 1         #Add instruction
    MUL = 2         #Multiple instruction
    IN = 3          #Input instruction
    OUT = 4         #Output instruction
    JMP_IF = 5      #Jump to instruction pointer if true
    JMP_ELSE = 6    #Jump to instruction pointer if false
    LE = 7          #Return 1 if less than instruction
    EQ = 8          #Return 1 if equal than instruction
    IRB = 9         #Increment relative base pointer instruction
    HLT = 99        #Halt instruction    

class OpMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class IntCodeMachine:

    def __init__(self, program, io_in=None, io_out=None, memory=0):

        self.stack = program + [0] * memory
        self.ip = 0
        self.relative_base = 0
        self.halted = False

        self.io_i = io_in if io_in is not None else deque()
        self.io_o = io_out if io_out is not None else deque()

    def set_input_source(self, new_input):
        self.io_i = new_input

    def feed_inputs(self, inputs):
        self.io_i.extend(inputs)

    def out(self):
        return self.io_o.popleft()

    def out_latest(self):
        return self.io_o.pop()

    def _parse_op_modes(self, instruction):
        """
        ABCDE
         1002

        DE - two-digit opcode,      02 == opcode 2
        C - mode of 1st parameter,  0 == position mode
        B - mode of 2nd parameter,  1 == immediate mode
        A - mode of 3rd parameter,  0 == position mode,
                                        omitted due to being a leading zero

        For simplicity we just read max amount of params modes,
        instead of reading only modes used by operation.
        """
        
        #defaults
        param1mode = OpMode.POSITION
        param2mode = OpMode.POSITION
        param3mode = OpMode.POSITION
        
        op = instruction % 100
        instruction //= 100

        param1mode = instruction % 10
        instruction //= 10

        param2mode = instruction % 10
        instruction //= 10
        
        param3mode = instruction % 10
        #end of instruction

        return op, param1mode, param2mode, param3mode

    def _parse_params_with_mode(self, at, mode):

        if mode == OpMode.IMMEDIATE:
            return self.stack[at]
        elif mode == OpMode.POSITION:
            return self.stack[self.stack[at]]
        elif mode == OpMode.RELATIVE:
            return self.stack[self.relative_base + self.stack[at]]
        else:
            raise ValueError('Unknown parameter mode {mode}. This is fatal.')

    def _parse_position_with_mode(self, at, mode):
        """ A stopgap solution """
        if mode == OpMode.POSITION:
            val = self.stack[at]
        else: #relative mode
            val = self.relative_base + self.stack[at]
        return val

    def __iter__(self):
        return iter(self.run())

    def run(self):
    
        while not self.halted:
            op, param1mode, param2mode, param3mode = self._parse_op_modes(self.stack[self.ip])
            self.ip += 1

            if op == OpCode.HLT:
                self.halted = True
                break

            elif op == OpCode.ADD:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)
                param3 = self._parse_position_with_mode(self.ip+2, param3mode)

                res = param1 + param2
                self.stack[param3] = res
                self.ip += 3

            elif op == OpCode.MUL:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)
                param3 = self._parse_position_with_mode(self.ip+2, param3mode)
                
                res = param1 * param2
                self.stack[param3] = res
                self.ip += 3

            elif op == OpCode.IN:
                param1 = self._parse_position_with_mode(self.ip, param1mode)

                if not len(self.io_i):
                    self.ip -= 1
                    return
                else:
                    self.stack[param1] = self.io_i.popleft()
                    self.ip += 1

            elif op == OpCode.OUT:
                param1 = self._parse_params_with_mode(self.ip, param1mode)

                self.io_o.append(param1)
                self.ip += 1

            elif op == OpCode.JMP_IF:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)
        
                if param1 != 0:
                    self.ip = param2
                else:
                    self.ip += 2

            elif op == OpCode.JMP_ELSE:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)

                if param1 == 0:
                    self.ip = param2
                else:
                    self.ip += 2

            elif op == OpCode.LE:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)
                param3 = self._parse_position_with_mode(self.ip+2, param3mode)

                self.stack[param3] = int(param1 < param2)

                self.ip += 3

            elif op == OpCode.EQ:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                param2 = self._parse_params_with_mode(self.ip+1, param2mode)
                param3 = self._parse_position_with_mode(self.ip+2, param3mode)

                self.stack[param3] = int(param1 == param2)
                    
                self.ip += 3
            
            elif op == OpCode.IRB:
                param1 = self._parse_params_with_mode(self.ip, param1mode)
                self.relative_base += param1
                self.ip += 1

            else:

                raise ValueError(f'Invalid OpCode: {op}.')

            yield

""" A method for single whole run of IntCodeMachine, preserved for backward compat reasons. """
def run(instructions, *args, starting_pos=0, jmp_width=4, **kwargs):
    inputs = kwargs.get('inputs', [])
    outputs = kwargs.get('outputs', [])
    m = IntCodeMachine(instructions, io_in=deque(inputs), io_out=outputs)
    
    #Usage with controlling outerloop
    #
    # while True: 
    #     try:
    #         next(iter(m))
    #     except:
    #         break
    
    for _ in m.run():
        pass
    
    return m.stack

"""
Todo: 
    + DONE
    - PENDING
    * PLANNED
    ? UNSURE

    +copy old day_2 tests to this as legacy.
    +Refactor such that old tests pass with new logic where opcode is parsed and appropriate amount of params are read from stack and stack pointer is incremented accordingly. This should not need a out-of-bounds indexing exception handling like in previous version
    +Add new instruction for IO
    +Add operational modes
    +Parse opcodes to determine parameter modes
    +TASK 1 COMPLETE
    +Add JMP and Comparision instructions and needed opcodes
    +Add tests to JMP and COMP instructions
    +TASK 2 COMPLETE

    +This needs to be turned into a class
"""
if __name__ == "__main__":
    
    def print_diagnostic_messages(sys_id:int, sys_name:str, buffer_list):
        print(f'Printing diagnostic codes for ship\'s {sys_name} (sys ID: {sys_id}). \n ----------------')
        for line in buffer_list:
            print(line)

    program = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,57,23,224,101,-1311,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1102,57,67,225,102,67,150,224,1001,224,-2613,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,2,179,213,224,1001,224,-469,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1001,188,27,224,101,-119,224,224,4,224,1002,223,8,223,1001,224,7,224,1,223,224,223,1,184,218,224,1001,224,-155,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,21,80,224,1001,224,-101,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1101,67,39,225,1101,89,68,225,101,69,35,224,1001,224,-126,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,7,52,225,1102,18,90,225,1101,65,92,225,1002,153,78,224,101,-6942,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,67,83,225,1102,31,65,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,226,226,224,102,2,223,223,1005,224,329,1001,223,1,223,108,677,226,224,1002,223,2,223,1005,224,344,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,359,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,419,1001,223,1,223,107,677,226,224,102,2,223,223,1006,224,434,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,539,1001,223,1,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,629,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,644,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226]

    # Part 1
    io_in = [1]
    io_out = []

    run(program.copy(), inputs=io_in, outputs=io_out)

    print_diagnostic_messages(1, 'air conditioner unit', io_out)

    # Part 2
    io_in = [5]
    io_out.clear()

    run(program.copy(), inputs=io_in, outputs=io_out)

    print_diagnostic_messages(5, 'thermal radiator controller', io_out)