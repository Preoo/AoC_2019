from enum import IntEnum
from collections import deque

class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JMP_IF = 5
    JMP_ELSE = 6
    LE = 7
    EQ = 8
    HLT = 99

class OpMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

""" A single function should suffice for these tasks, this could have been better served as a class thought. """
def run(instructions, *args, starting_pos=0, jmp_width=4, **kwargs):

    stack = instructions
    ip = starting_pos

    #IO queues
    if 'inputs' in kwargs:
        input_deque = deque(kwargs['inputs'])
    output = kwargs.get('outputs', [])

    def _parse_op_modes(instruction):
        """
        ABCDE
         1002

        DE - two-digit opcode,      02 == opcode 2
        C - mode of 1st parameter,  0 == position mode
        B - mode of 2nd parameter,  1 == immediate mode
        A - mode of 3rd parameter,  0 == position mode,
                                        omitted due to being a leading zero

        For simplicity we just read max amount of params modes, instead of reading only modes used by operation.
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

    while True:
        op, param1mode, param2mode, param3mode = _parse_op_modes(stack[ip])
        ip += 1

        if op == OpCode.HLT:
            break

        elif op == OpCode.ADD:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]

            assert param3mode == OpMode.POSITION, f'Parameter for writing must be in position mode'
            
            param3 = stack[ip+2]

            res = param1 + param2
            stack[param3] = res
            ip += 3

        elif op == OpCode.MUL:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]

            assert param3mode == OpMode.POSITION, f'Parameter for writing must be in position mode'
            
            param3 = stack[ip+2]
            
            res = param1 * param2
            stack[param3] = res
            ip += 3

        elif op == OpCode.IN:
            assert param1mode == OpMode.POSITION, f'Parameter for writing must be in position mode'
            param1 = stack[ip]

            stack[param1] = input_deque.popleft()
            ip += 1

        elif op == OpCode.OUT:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]

            output.append(param1)
            ip += 1

        elif op == OpCode.JMP_IF:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]
    
            if param1 != 0:
                ip = param2
            else:
                ip += 2

        elif op == OpCode.JMP_ELSE:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]

            if param1 == 0:
                ip = param2
            else:
                ip += 2

        elif op == OpCode.LE:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]

            assert param3mode == OpMode.POSITION, f'Parameter for writing must be in position mode'
            
            param3 = stack[ip+2]

            if param1 < param2:
                stack[param3] = 1
            else:
                stack[param3] = 0

            ip += 3

        elif op == OpCode.EQ:
            param1 = stack[ip] if param1mode == OpMode.IMMEDIATE else stack[stack[ip]]
            param2 = stack[ip+1] if param2mode == OpMode.IMMEDIATE else stack[stack[ip+1]]

            assert param3mode == OpMode.POSITION, f'Parameter for writing must be in position mode'
            
            param3 = stack[ip+2]

            if param1 == param2:
                stack[param3] = 1
            else:
                stack[param3] = 0
                
            ip += 3

        else:
            #Exception state, unknown opcode
            raise ValueError(f'Invalid OpCode: {op}.')

    return stack

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

    ?Refactor from single method to a class based design
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