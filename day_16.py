from typing import List, Union
import numpy as np
from math import ceil

"""
Part 1 was done by using bruteforce with numpy OR by creating multiplier on fly by using generators
Part 2 was done with help of internet :/ I wasn't good enough
"""
def pattern_generator(base_pattern:List[int], nth_element:int, input_len:int):
    # generator which yields multipliers for nth_element in output.
    # use this a part of summing operation
    k = nth_element
    for i in range(input_len):
        yield base_pattern[(i+1)//(k+1)%4]

def FFT2(input_signal:Union[List[int], str], base_pattern:List[int] = [0, 1, 0, -1], phases:int = 1) -> List[int]:
    # Instead of generating a list of multipliers (a last resort), try to write a generator for that.
    # def gen(N, nth_elem, base_pattern=[n,n,n,n])
    signal = input_signal if isinstance(input_signal, list) else [int(d) for d in input_signal]
    len_input = len(input_signal)

    # Both of these work but are slow

    for _ in range(phases):
        print(f'.', end='', flush=True)
        signal = [
            abs(sum((s*p for s,p in zip(signal, pattern_generator(base_pattern, nth_elem, len_input))))) % 10 
            for nth_elem in range(len_input)]
    print('')
    return signal
    # signal = np.fromiter(signal, int)
    # temp = np.zeros_like(signal)
    # for _ in range(phases):
    #     print('!', end='', flush=True)
    #     for nth_elem in range(len_input):
    #         # temp[nth_elem] = np.dot(signal, np.fromiter(pattern_generator(base_pattern, nth_elem, len_input), int, len_input))
    #         temp[nth_elem] = sum([signal[i] * g for i, g in enumerate(pattern_generator(base_pattern, nth_elem, len_input))])
    #     signal = np.mod(np.abs(temp), 10)
    # return list(signal)

# Using numpy may be fast but part 2 input is so big, it ate 16gb for breakfast, try something else instead
def FFT(input_signal:Union[List[int], str], base_pattern:List[int] = [0, 1, 0, -1], phases:int = 1) -> List[int]:
    signal = input_signal if isinstance(input_signal, list) else (int(d) for d in input_signal)
    len_input = len(input_signal)
    signal = np.fromiter(signal, int)
    print('Creating pattern')
    # This is grows too fast mem-wise, for part 2 another solution is needed
    pattern = np.array([generate_pattern_for_element(base_pattern, nth, len_input) for nth in range(1, len_input + 1)])
    
    print('Starting calc')
    for _ in range(phases):
        np.sum(signal * pattern, axis=1, out=signal)
        np.mod(np.abs(signal), 10, out=signal)

    return list(signal)

def generate_pattern_for_element(base_pattern:List[int], nth_element:int, len_input:int):
    
    hack = np.array(base_pattern, dtype=int)
    pattern = np.repeat(hack, nth_element)
    tiles = ceil(len_input / len(pattern)) + 1
    return np.tile(pattern, tiles)[1:len_input + 1]

def FFT3(input_signal:Union[List[int], str], base_pattern:List[int] = [0, 1, 0, -1], phases:int = 1) -> List[int]:
    d = input_signal if isinstance(input_signal, list) else [int(d) for d in input_signal]
    for _ in range(phases):
        print(f'.', end='', flush=True)
        for i in range(len(d) -1 , 0, -1):
            d[i-1] = (d[i - 1] + d[i]) % 10
    print('')
    return d

def part1(puzzle_input):
    res = FFT2(puzzle_input, phases=100)
    ans = ''.join((str(d) for d in res[:8]))
    # Correct answer was 52611030
    print(f'Part 1 answer: {ans}')

def part2(puzzle_input):
    offset:str = puzzle_input[:7]
    offset = int(offset)
    res = FFT3(puzzle_input * 10_000, phases=100)
    ans = res[offset : offset + 8]
    # Correct answer was 52541026
    print(f'Part 2 answer: {"".join(map(str, ans))}')

def main():
    puzzle_input = '59780176309114213563411626026169666104817684921893071067383638084250265421019328368225128428386936441394524895942728601425760032014955705443784868243628812602566362770025248002047665862182359972049066337062474501456044845186075662674133860649155136761608960499705430799727618774927266451344390608561172248303976122250556049804603801229800955311861516221350410859443914220073199362772401326473021912965036313026340226279842955200981164839607677446008052286512958337184508094828519352406975784409736797004839330203116319228217356639104735058156971535587602857072841795273789293961554043997424706355960679467792876567163751777958148340336385972649515437'
    part1(puzzle_input)
    part2(puzzle_input)
if __name__ == "__main__":
    main()