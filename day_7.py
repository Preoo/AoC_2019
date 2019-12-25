import day_5 as opcode_machine
from itertools import permutations


if __name__ == "__main__":
    program = [3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99]

    #Part 1
    phase_settings = set(permutations(range(5)))

    thruster_signals = set()
    
    for phase_setting in phase_settings:
        input_signal = [0]
        outputs = []
        for i, amplifier in enumerate(['A', 'B', 'C', 'D', 'E']):
            outputs.clear()
            opcode_machine.run(program.copy(), inputs=[phase_setting[i]] + input_signal, outputs=outputs)

            #print(f'Amplifier {amplifier} return signal {outputs} for input {input_signal} and phase {phase_setting[i]}.')

            input_signal = outputs.copy()
    
        thruster_signals.add(outputs[0])

    print(f'Max thruster signal is {max(thruster_signals)}')

    #Part 2
    phase_settings = set(permutations(range(5, 10)))

    from day_5 import IntCodeMachine as m

    test_prog = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    test_phase = [9,7,8,5,6]

    thruster_signals.clear()

    for phase_setting in phase_settings:

        machines = [m(program.copy()) for _ in range(5)]
        for i in range(5):
            machines[i].set_input_source(machines[i-1].io_o)
        

        for mc, p in zip(machines, phase_setting):
            mc.feed_inputs([p])

        machines[0].feed_inputs([0])

        while not machines[-1].halted:
            for i, ma in enumerate(machines):
                for _ in ma.run():
                    pass
                
        print(machines[-1].io_o)
        thruster_signals.add(machines[-1].io_o[0])
        
    print(f'Max thruster signal is {max(thruster_signals)}')        
