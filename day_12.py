import numpy as np
from itertools import combinations, permutations
from math import gcd

class Moon:
    def __init__(self, x=0, y=0, z=0):
        self.pos = np.array([x, y, z], dtype=np.int64)
        self.vel = np.zeros_like(self.pos)

    def update(self, new_vel):
        """ Update moons pos and velocity according to new velocity <new_vel> """
        self.vel += new_vel
        self.pos += self.vel

    def get_total_energy(self):
        return np.sum(np.abs(self.pos)) * np.sum(np.abs(self.vel))

    def __repr__(self):
        return f'Moon(pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>)'

class System:
    def __init__(self, moons):
        self.moons = moons if moons else list()

    def simulate(self, n=10):
        for tick in range(n):
            yield tick, self.moons

            # This won't be easily modified to suit part 2 :(
            moon_stack = np.stack([moon.pos for moon in self.moons])
            for moon in self.moons:
                new_vel = np.sum(np.sign(moon_stack + np.negative(moon.pos)), axis=0)
                moon.update(new_vel)

    def simulate_on_axis(self, axis):
        tick = 0
        
        _pos = [moon.pos[axis] for moon in self.moons]
        _vel = [moon.vel[axis] for moon in self.moons]
        
        idx = [0, 1, 2, 3]

        while True:  
            for i, j in combinations(idx, 2):
                
                if _pos[i] < _pos[j]:
                    _vel[i] += 1
                    _vel[j] -= 1
                elif _pos[i] > _pos[j]:
                    _vel[i] -= 1
                    _vel[j] += 1

            _pos[0] += _vel[0]
            _pos[1] += _vel[1]
            _pos[2] += _vel[2]
            _pos[3] += _vel[3]
            tick += 1

            if _vel[0] == 0 and _vel[1] == 0 and _vel[2] == 0 and _vel[3] == 0:
                break

        return tick * 2


    def total_energy_in_system(self):
        return sum((moon.get_total_energy() for moon in self.moons))

def main():
    io = Moon(x=-17, y=9, z=-5)
    europa = Moon(x=-1, y=7, z=13)
    ganymede = Moon(x=-19, y=12, z=5)
    callisto = Moon(x=-6, y=-6, z=-4)
    system = System([io, europa, ganymede, callisto])
    
    # Part 1
    n_ticks = 1000
    for tick, moons in system.simulate(n=n_ticks):
        pass

    print(f'Total energy in system after {n_ticks} ticks is {system.total_energy_in_system()}.')
    part1_answer = system.total_energy_in_system()
    # Part 2
    """
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    expected steps: 2772

    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>
    expected steps: 4686774924
    """

    io = Moon(x=-17, y=9, z=-5)
    europa = Moon(x=-1, y=7, z=13)
    ganymede = Moon(x=-19, y=12, z=5)
    callisto = Moon(x=-6, y=-6, z=-4)
    system = System([io, europa, ganymede, callisto])

    
    test1 = system.simulate_on_axis(0)
    test2 = system.simulate_on_axis(1)
    test3 = system.simulate_on_axis(2)

    def lcm(a, b):
        return a * b // gcd(a, b)

    print(f'LCM: {lcm(test1, lcm(test2, test3))}')
    part2_answer = lcm(test1, lcm(test2, test3))

    # for tests
    return part1_answer, part2_answer

if __name__ == "__main__":

    main()