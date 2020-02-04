from Shared.IntCodeMachine import machine as opcode_machine
from itertools import permutations

def main():
    program = [3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99]

    #Part 1
    phase_settings = set(permutations(range(5)))
    thruster_signals = set()
    
    for phase_setting in phase_settings:
        input_signal = [0]
        outputs = []
        for i, _ in enumerate(['A', 'B', 'C', 'D', 'E']):
            outputs.clear()
            opcode_machine.run(program.copy(), inputs=[phase_setting[i]] + input_signal, outputs=outputs)
            input_signal = outputs.copy()
    
        thruster_signals.add(outputs[0])

    print(f'Part 1: Max thruster signal is {max(thruster_signals)}')
    part1_answer = max(thruster_signals)

    #Part 2
    phase_settings = set(permutations(range(5, 10)))
    thruster_signals.clear()

    for phase_setting in phase_settings:

        machines = [opcode_machine.IntCodeMachine(program.copy()) for _ in range(5)]
        for i in range(5):
            machines[i].set_input_source(machines[i-1].io_o)
        
        for mc, p in zip(machines, phase_setting):
            mc.feed_inputs([p])

        machines[0].feed_inputs([0])

        while not machines[-1].halted:
            for i, ma in enumerate(machines):
                for _ in ma.run():
                    pass
                
        thruster_signals.add(machines[-1].io_o[0])
        
    print(f'Part 2: Max thruster signal is {max(thruster_signals)}')   
    part2_answer = max(thruster_signals)

    return part1_answer, part2_answer

if __name__ == "__main__":
    main()