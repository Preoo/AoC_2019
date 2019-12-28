from dataclasses import dataclass
from pathlib import Path
from math import sqrt, gcd

# allow creation of hashable dataclass 
@dataclass(eq=True, frozen=True)
class Asteroid:
    x: int
    y: int

    # def is_colinear_with(self, origin, other):
    #     """ Is this asteroid on same line as origin and other. """
    #     return (origin.x - self.x) * (other.y - self.y) == (other.x - self.x) * (origin.y - self.y)

    # def has_same_direction(self, origin, other):
    #     """ Kindergarden test to see if this is behind origin therefore kept in set, assuming they are colinear. """
    #     x_dir, y_dir = False, False
    #     #case: x-axis
    #     if other.x > origin.x:
    #         x_dir = self.x > origin.x
    #     else:
    #         x_dir = self.x < origin.x

    #     #case: y-axis
    #     if other.y > origin.y:
    #         y_dir = self.y > origin.y
    #     else:
    #         y_dir = self.y < origin.y

    #     #if both hold -> self is in same direction
    #     return x_dir and y_dir

# Parse map to set of Astroids with x,y coords
def parse_asteroidmap(asteroidmap):
    asteroids = set()

    for y, line in enumerate(asteroidmap.splitlines()):
        for x, thing in enumerate(line):
            if thing == '#': asteroids.add(Asteroid(x,y))
    
    return asteroids

# Pretty print map
def print_asteroidmap(width, height):
    raise NotImplementedError

def find_optimal_observatory(asteroidmap):
    asteroids = parse_asteroidmap(asteroidmap)
    asteroid_los_from_ast = dict()
    # colinear_with_candidate = set()
    # for candidate in asteroids:
    #     colinear_with_candidate.clear()
    #     possible_locations = asteroids - set([candidate])
    #     asteroid_los_from_ast[candidate] = len(possible_locations)

    #     while len(possible_locations):
            
    #         other = possible_locations.pop()
    #         colinear_with_candidate.add(other)
            
    #         for others in possible_locations:
    #             if others.is_colinear_with(candidate, other) and others.has_same_direction(candidate, other):
    #                 colinear_with_candidate.add(others)
    #                 asteroid_los_from_ast[candidate] -= 1

            
    #         possible_locations -= colinear_with_candidate
    
    for candidate in asteroids:
        possible_locations = asteroids - set([candidate])
        assert candidate not in possible_locations
        sloaps_to_target = set()

        # thanks https://github.com/kresimir-lukin/AdventOfCode2019/blob/master/day10.py
        for target in possible_locations:
            dx, dy = target.x - candidate.x, target.y - candidate.y
            dx, dy = dx // gcd(dx, dy), dy // gcd(dx, dy)
            sloaps_to_target.add((dx, dy))

        asteroid_los_from_ast[candidate] = len(sloaps_to_target)

    print(asteroid_los_from_ast)
    best_asteroid = max(asteroid_los_from_ast, key=asteroid_los_from_ast.get)
    return best_asteroid, asteroid_los_from_ast[best_asteroid]


if __name__ == "__main__":
    puzzle_input = Path('input/day_10').read_text()

    a, c = find_optimal_observatory(puzzle_input)
    print(f'Asteroid: {a} with line of sight to {c} other asteroids.')
    #17,23 : 324 !too high
    #21,9 : 310 !too high
    #17,23 : 296 !ok

