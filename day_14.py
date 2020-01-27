from pathlib import Path
from math import ceil
from dataclasses import dataclass
from typing import List
from collections import defaultdict, deque

@dataclass
class Elem:
    amount:int
    material:str

@dataclass
class Reaction:
    produced:Elem
    consumed:List[Elem]

def parse_reactions(from_string:str) -> List[Reaction]:

    def create_element(element_string:str) -> Elem:
        amount, element = element_string.split(' ')
        return Elem(int(amount), element)

    reactions = []
    for reaction in from_string.splitlines():
        consumed, produced = reaction.split(' => ')
        produced = create_element(produced)
        consumed = [create_element(e) for e in consumed.split(', ')]
        reactions.append(Reaction(produced, consumed))
        
    return reactions

def required_ore(from_string:str, fuel:int = 1) -> int:
    reactions = parse_reactions(from_string)
    surplus = defaultdict(int)

    """Queue based solution 5/5 testcases passed
        Assumptions: 
            there are no deadend reaction chains, we assume all paths leads to ORE
            there are no useless reactions left as results from expanding from * => 1 FUEL
            there is no previous surplus of materials
            there is only single reaction for each produced element, else reaction filtering would     only return first such occurance
        Notes:
            Part 2 may need a binary search
            Or bruteforce with parallelprocessing, perhaps both and a benchmark?
            Apparently this could also be solved with linear solver
    """
    pending_reactions = deque()
    pending_reactions.append(Elem(fuel, 'FUEL'))
    ores = 0

    while len(pending_reactions):
        elem = pending_reactions.popleft()
        if elem.material == 'ORE':
            ores += elem.amount
        elif surplus[elem.material] >= elem.amount:
            surplus[elem.material] -= elem.amount
        else:
            amount_required = elem.amount - surplus[elem.material]
            reaction = [r for r in reactions if r.produced.material == elem.material].pop()
            times = ceil(amount_required / reaction.produced.amount)
            pending_reactions.extend(reaction.consumed * times)
            surplus[elem.material] = (times * reaction.produced.amount) - amount_required
            
    return ores

def most_fuel_per_trillion_ore(conversion_process:str, lower_bound:int = 1):
    """ Can't just divide, as overlow of ORE could be used to create more than that. """
    cargo_capacity = 1000000000000
    return cargo_capacity / 2486514

if __name__ == "__main__":
    puzzle_input = Path('input/day_14').read_text()
    part1_answer = required_ore(puzzle_input)
    print(f'{part1_answer=}')
    part2_answer = most_fuel_per_trillion_ore(puzzle_input, lower_bound=part1_answer)
    print(f'{part2_answer=}')