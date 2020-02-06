from typing import List, Union
import numpy as np
from math import ceil

def FFT(input_signal:Union[List[int], str], base_pattern:List[int] = [0, 1, 0, -1], phases:int = 1) -> List[int]:
    signal = input_signal if isinstance(input_signal, list) else [int(d) for d in input_signal]
    len_input = len(input_signal)

    for _ in range(phases):
        signal = apply_FFT(signal, base_pattern)
        assert len(signal) == len_input

    return signal

def apply_FFT(signal:List[int], base_pattern:List[int]) -> List[int]:
    pattern = np.array([generate_pattern_for_element(base_pattern, nth, len(signal)) for nth in range(1, len(signal) + 1)])
    signal_np = np.array(signal, dtype=int)
    # r = signal_np * pattern # should be of shape input_len x input_len
    # sum over columns (axis=1) -> to get elements
    results = np.sum(signal_np * pattern, axis=1) # should be 1D array of input_len
    return list(np.abs(results) % 10) # if results[n] is negative, this yields something else

def generate_pattern_for_element(base_pattern:List[int], nth_element:int, len_input:int) -> List[int]:
    # TODO: return List[int] or numpy array ??
    hack = np.array(base_pattern, dtype=int)
    pattern = np.repeat(hack, nth_element)
    tiles = ceil(len_input / len(pattern)) + 1
    return np.tile(pattern, tiles)[1:len_input + 1]

def part1(puzzle_input):
    res = FFT(puzzle_input, phases=100)
    ans = ''.join((str(d) for d in res[:8]))
    # Correct answer was 52611030
    print(f'Part 1 answer: {ans}')

def part2(puzzle_input):
    offset:str = puzzle_input[:7]
    res = FFT(puzzle_input, phases=100)
    ans = res[int(offset):int(offset) + 8]
    print(f'Part 2 answer: {ans}')

def main():
    puzzle_input = '59780176309114213563411626026169666104817684921893071067383638084250265421019328368225128428386936441394524895942728601425760032014955705443784868243628812602566362770025248002047665862182359972049066337062474501456044845186075662674133860649155136761608960499705430799727618774927266451344390608561172248303976122250556049804603801229800955311861516221350410859443914220073199362772401326473021912965036313026340226279842955200981164839607677446008052286512958337184508094828519352406975784409736797004839330203116319228217356639104735058156971535587602857072841795273789293961554043997424706355960679467792876567163751777958148340336385972649515437'
    part1(puzzle_input)
    part2(puzzle_input * int(1e4))
if __name__ == "__main__":
    main()