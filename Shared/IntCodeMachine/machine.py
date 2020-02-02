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