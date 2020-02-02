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
            reaction = next(filter(lambda r: r.produced.material == elem.material, reactions))
            times = ceil(amount_required / reaction.produced.amount)
            #pending_reactions.extend(reaction.consumed * times) # Trying to save lines costs too much performance to allocations
            for r in reaction.consumed:
                pending_reactions.append(Elem(r.amount * times, r.material))
            surplus[elem.material] = (times * reaction.produced.amount) - amount_required
            
    return ores

def get_fuel_yield_from_carge(conversion_process:str, lower_bound:int = 1, upper_bound:int = 1000000, cargo_capacity:int = 1000000000000) -> int:
    """
    Basic binary search to find max FUEL production for given cargo capacity.
    Upper_bound was found by testing, it yields slighly larger values than default cargo capacity.
    """
    
    _low = lower_bound
    _high = upper_bound
    _mid = (upper_bound + lower_bound) // 2
    guess = required_ore(conversion_process, fuel=_mid)
    while _low <= _high:
        if guess > cargo_capacity:
            _high = _mid - 1
            _mid = (_high + _low) // 2
        elif guess < cargo_capacity:
            _low = _mid + 1
            _mid = (_high + _low) // 2
        else:
            return _mid
        
        guess = required_ore(conversion_process, fuel=_mid)

    return _mid

if __name__ == "__main__":
    puzzle_input = Path('input/day_14').read_text()
    part1_answer = required_ore(puzzle_input)
    print(f'{part1_answer=}')
    # Set lower bound for search to be amount of ORE needed for one FUEL
    part2_answer = get_fuel_yield_from_carge(puzzle_input, lower_bound=int(1e12 // part1_answer))
    print(f'{part2_answer=}')
    
    # Correct answers:
    #   part1_answer=2486514
    #   part2_answer=998536