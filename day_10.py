from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict
from math import sqrt, gcd, atan2, acos, degrees

# allow creation of hashable dataclass 
@dataclass(eq=True, frozen=True)
class Asteroid:
    x: int
    y: int

    def distance_to(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

def angle_between(asteroid, laser_station):
    """ Angle between one and other given shared origin """
    # New info in form of atan2, had to looks this one up.
    return -atan2(asteroid.x - laser_station.x, asteroid.y - laser_station.y)

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
    
    for candidate in asteroids:
        possible_locations = asteroids - set([candidate])
        assert candidate not in possible_locations
        sloaps_to_target = set()

        # thanks to https://github.com/kresimir-lukin/AdventOfCode2019/blob/master/day10.py
        for target in possible_locations:
            dx, dy = target.x - candidate.x, target.y - candidate.y
            dx, dy = dx // gcd(dx, dy), dy // gcd(dx, dy)
            sloaps_to_target.add((dx, dy))

        asteroid_los_from_ast[candidate] = len(sloaps_to_target)

    best_asteroid = max(asteroid_los_from_ast, key=asteroid_los_from_ast.get)
    return best_asteroid, asteroid_los_from_ast[best_asteroid]

def evaporate_asteroid_field(map_asteroid_field, firing_position):
    asteroid_field = parse_asteroidmap(map_asteroid_field)
    asteroid_field.remove(firing_position)
    dist_angle_map = defaultdict(list)
    

    for asteroid in asteroid_field:
        # This challenge kicked my ass, thanks https://github.com/kresimir-lukin/AdventOfCode2019/blob/master/day10.py
        dx, dy = asteroid.x - firing_position.x, asteroid.y - firing_position.y
        dx, dy = dx // gcd(dx, dy), dy // gcd(dx, dy)
        angle = angle_between(asteroid, firing_position)
        dist_angle_map[angle].append(asteroid)
    
    for v in dist_angle_map.values():
        v.sort(key=lambda x: x.distance_to(firing_position))

    sorted_list = sorted(dist_angle_map)

    order_list = []
    while len(order_list) != len(asteroid_field):
        for k in sorted_list:
            if len(dist_angle_map[k]):
                order_list.append(dist_angle_map[k].pop(0))

    return order_list

if __name__ == "__main__":
    puzzle_input = Path('input/day_10').read_text()

    a, c = find_optimal_observatory(puzzle_input)
    print(f'Asteroid: {a} with line of sight to {c} other asteroids.')

    a = evaporate_asteroid_field(puzzle_input, a)[200 - 1]
    print(f'Solution could be: {a.x*100 + a.y} ?')