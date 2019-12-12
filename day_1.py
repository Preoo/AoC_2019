from typing import Sequence
from pathlib import Path


def get_fuel_from_weight(weight:int) -> int:
    fuel = weight // 3 - 2
    if fuel > 0: 
        return fuel
    else:
        return 0

def calc_fuel(values, *args, **kwargs) -> int:
    total = 0
    for weight in values:
        total += get_fuel_from_weight(weight)
    return total

def calc_fuel_for_fuel(fuel_weight):
    
    additional_fuel = get_fuel_from_weight(fuel_weight)
    if additional_fuel > 0:
        return additional_fuel + calc_fuel_for_fuel(additional_fuel)
    else:
        return additional_fuel

def get_input_from_str(from_string:str) -> Sequence[int]:
    lines = from_string.strip().splitlines()
    return list(map(lambda x: int(x), lines))

def get_input_from_file(from_file:Path) -> Sequence[int]:
    with open(from_file) as f:
        for line in f:
            # if line == '':
            #     raise StopIteration
            yield int(line)

if __name__ == "__main__":
    #Actually calculate answer
    filepath = Path('input/day_1')
    masses = get_input_from_file(filepath)
    fuel = calc_fuel(masses)
    print(f'Required fuel for problem: {fuel}.')

    #part 2
    masses = get_input_from_file(filepath)
    more_fuel = sum(calc_fuel_for_fuel(x) for x in masses)
    print(f'After adjusting for fuel weight, we got total: {more_fuel}.')