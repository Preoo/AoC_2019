from enum import IntEnum

class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    HLT = 99

""" A single function should suffice for this task """
def run(instructions, starting_pos=0, jmp_width=4):
    #Naive detection of contious loops, without end
    halting_threshold = 1000
    halting_counter = 0

    stack = instructions
    ip = starting_pos
    (op, param1, param2, ret) = stack[ip:ip+jmp_width]
    
    while op != OpCode.HLT:

        if op == OpCode.ADD:
            res = stack[param1] + stack[param2]
            stack[ret] = res
        elif op == OpCode.MUL:
            res = stack[param1] * stack[param2]
            stack[ret] = res
        else:
            #Exception state, unknown opcode
            raise ValueError(f'Invalid OpCode: {op}.')
        halting_counter += 1
        if halting_counter > halting_threshold:
            print(f'Loops threshold exceeded, aborting to save santa')
            break
        ip += jmp_width
        try:
            (op, param1, param2, ret) = stack[ip:ip+jmp_width]
        except ValueError:
            #print(f'Reached end of stack, terminating.')
            break

    return stack

if __name__ == "__main__":
    instructions = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,19,10,23,1,23,13,27,1,6,27,31,1,9,31,35,2,10,35,39,1,39,6,43,1,6,43,47,2,13,47,51,1,51,6,55,2,6,55,59,2,59,6,63,2,63,13,67,1,5,67,71,2,9,71,75,1,5,75,79,1,5,79,83,1,83,6,87,1,87,6,91,1,91,5,95,2,10,95,99,1,5,99,103,1,10,103,107,1,107,9,111,2,111,10,115,1,115,9,119,1,13,119,123,1,123,9,127,1,5,127,131,2,13,131,135,1,9,135,139,1,2,139,143,1,13,143,0,99,2,0,14,0]

    #Task specific alternations
    instructions[1] = 12
    instructions[2] = 2

    #Step through excecution
    output = run(instructions)

    print(f'After halting, position 0 has value {output[0]}.')

    #Task 2 
    expected_value_of_pos0 = 19690720
    nouns = range(100)
    verbs = range(100)
    possible_answers = []

    instructions = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,19,10,23,1,23,13,27,1,6,27,31,1,9,31,35,2,10,35,39,1,39,6,43,1,6,43,47,2,13,47,51,1,51,6,55,2,6,55,59,2,59,6,63,2,63,13,67,1,5,67,71,2,9,71,75,1,5,75,79,1,5,79,83,1,83,6,87,1,87,6,91,1,91,5,95,2,10,95,99,1,5,99,103,1,10,103,107,1,107,9,111,2,111,10,115,1,115,9,119,1,13,119,123,1,123,9,127,1,5,127,131,2,13,131,135,1,9,135,139,1,2,139,143,1,13,143,0,99,2,0,14,0]

    print(f'Trying to find noun and verb which yield as inputs a output value of {expected_value_of_pos0}')

    #Nested for loops, feelsweirdman
    for noun in nouns:
        for verb in verbs:
            #reset
            state = instructions.copy() #simply assinging will just create a reference to lvalue
            #apply inputs
            state[1] = noun
            state[2] = verb
            try:
                output = run(state)
            except ValueError:
                print(f'Invalid opcode for inputs: {noun} | {verb}. Skipping.')
                continue
            
            if output[0] == expected_value_of_pos0:
                possible_answers.append({
                    'noun' : noun,
                    'verb' : verb
                })

    #print(possible_answers)
    if len(possible_answers):
        for answer in possible_answers:
            print(f'What is 100 * noun + verb? Answer: 100 * {answer.get("noun")} + {answer.get("verb")} = {100 * answer.get("noun") + answer.get("verb")}')
    else:
        print(f'No answers :( )')