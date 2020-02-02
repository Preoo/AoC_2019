import subprocess
from pathlib import Path
from Shared.IntCodeMachine.machine import IntCodeMachine

#os.system('cls') if windows terminal and os.system('clear') if unix term
subprocess.run('clear')


puzzle_input = Path('input/day_13').read_text()
ping_pong_program = [int(x) for x in puzzle_input.split(',')]

#to play set value of address 0 to 2, else leave it as 0
ping_pong_program[0] = 2

cpu = IntCodeMachine(ping_pong_program.copy(), memory=10000)
# part_1_answer = 0
score = 0
paddle_coords = (0,0)
for _ in cpu.run():
    if len(cpu.io_o) == 3:
        x = cpu.out()
        y = cpu.out()
        val = cpu.out()
        if x == -1 and y == 0:
            score = val
        if val == 3: #new paddle position
            paddle_coords = (x, y)
            # print(f'Paddle pos: {paddle_coords}')
        if val == 4: #new ball position
            # print(f'Ball pos: {(x, y)}')
            if x < paddle_coords[0]:
                cpu.feed_inputs([-1])
            elif x > paddle_coords[0]:
                cpu.feed_inputs([1])
            else:
                cpu.feed_inputs([0])
        

# print(f'Block tiles count was {part_1_answer}')
print(f'Score: {score}')