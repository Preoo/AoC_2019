from pathlib import Path

'''
# Shower thought: model orbit graph as list of orbiters and list of all over orbits or vertices. Like this
class StarSystem:
    self.planets = [Planet_1, ..., Planet_n] #could be a set?
    self.orbits = [(Planet_1, Planet_n), ...] #could be a set?
    self.center_of_mass = < find planet m from orbits (x,y) in orbits such that m != y for all y = (x, y) in orbits >

    def __len__(self):
        return len(self.orbits)
    
    def add_orbit(other):
        union other with self.planets
        union other with self.orbits
    
    def __add__(other):
        decide if we add StarSystems together or merge new planets and orbits to self.
'''
class StarSystem:

    @classmethod
    def from_file(cls, input_as_file):
        with open(input_as_file) as f:
            #lines = [t for t in f.readlines() if t != '']
            return cls(f.readlines())

    @classmethod
    def from_string(cls, input_as_string:str):
        return cls(input_as_string.split('\n'))

    def __init__(self, orbits_iter, *args, **kwargs):
        self.stars = set()
        self.orbits = set()
        self.weights = {}
        
        self.add_orbits(orbits_iter)
        self.center_of_mass = self.find_center_mass()


    def add_orbits(self, orbits):
        for orbit in orbits:
            self.add_orbit(orbit.strip())

    def add_orbit(self, element:str, orbit_separator = ')'):
        
        parent, child = element.split(orbit_separator)
        self.stars.update([parent, child])
        self.orbits.add((parent,child))
        self.weights[(parent,child)] = 1

    def find_center_mass(self):

        set_of_orbiting_stars = set((s for _, s in self.orbits))
        com = self.stars - set_of_orbiting_stars
        assert len(com) == 1 #Assuming a single center of mass

        return com.pop()


    def get_total_orbits_to_COM(self, element):
        cost = 0
        current_pos = element

        while current_pos is not self.center_of_mass:
            for next_elem in self.stars:

                if (next_elem, current_pos) in self.orbits:
                    cost += self.weights[(next_elem, current_pos)]
                    current_pos = next_elem
        
        return cost

    def get_migration_hops(self, from_orbit, to_orbit):
        
        def get_hops(starting_pos):
            current_pos = starting_pos
            hops = set()

            while current_pos is not self.center_of_mass:
                for next_elem in self.stars:

                    if (next_elem, current_pos) in self.orbits:
                        hops.add((next_elem, current_pos))
                        current_pos = next_elem
            
            return hops

        difference = get_hops(from_orbit) ^ get_hops(to_orbit)

        return len(difference) - 2

    def __len__(self):
        ''' 
            Length of this object is count of all direct and indirect orbits 
        
        '''
        return sum(map(self.get_total_orbits_to_COM, self.stars))
        

if __name__ == "__main__":
    #This probably would have been as different implementation such as linked list node tree. Current implementation stems from concern that orbits won't form a proper tree. Current implementation has hints of directed graphs but they could be more formal... 

    # Part 1
    inputfile = Path('input/day_6')
    ss = StarSystem.from_file(inputfile)

    print(f'StarSystem has {len(ss)} orbits in total.')

    # Part 2 - XOR sets of hops between com, you and santa. Substract 2 to get answer

    print(f'Minimum number of orbital transfers required: {ss.get_migration_hops("YOU", "SAN")}')