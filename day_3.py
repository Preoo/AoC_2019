from pathlib import Path

class Panel:

    origin = (0,0)

    def __init__(self, *args, coils:dict, **kwargs):
        self.wires = []

        if coils:
            for wire, moves in coils.items():
                self.lay_wire((wire, moves))

    def lay_wire(self, coil):
        wire, moves = coil
        new_wire = Wire(wire)
        new_wire.lay(moves)
        self.wires.append(new_wire)

    def get_intersections(self):
        set0 = set(self.wires[0].steps[1:]) #skip first step (0,0)
        set1 = set(self.wires[1].steps[1:]) #skip first step (0,0)

        intersections = set0 & set1 #common points == intersections
        return intersections

    def get_closest_intersection_to_point(self, q=origin):

        intersections = self.get_intersections()
        distances = [manhattan_distance(p, q) for p in intersections]
        distances.sort()
        return distances[0]

class Wire:

    def __init__(self, name):
        self.steps = [(0,0)]
        self.name = name

        self.directions = {
            'U' : self.up,
            'D' : self.down,
            'L' : self.left,
            'R' : self.right
        }

    def lay(self, moves):
        for move in moves:
            self.step(move)

    def step(self, next_move:str):
        #For string U1, take first chr and lookup relevant function.
        # remaining chars should be casted to int and passed to that function as args.
        
        direction, *amount = next_move
        steps = int(''.join(amount))
        
        #This is a dirty hack to simplify intersection and length calculations. Wire keeps tabs for all points where it lays.
        for _ in range(steps):
            last_pos = self.steps[-1]
            new_pos = self.directions[direction](last_pos, 1)
            self.steps.append(new_pos)

    def up(self, pos, steps):
        #move up and return new point
        x, y = pos
        return (x , y + steps)

    def down(self, pos, steps):
        #move down and return new point
        x, y = pos
        return (x, y - steps)

    def left(self, pos, steps):
        #move left and return new point
        x, y = pos
        return (x - steps, y)

    def right(self, pos, steps):
        #move right and return new point
        x, y = pos
        return (x + steps, y)

def manhattan_distance(p, q):
    assert len(p) == len(q)
    d_1 = [abs(p_n - q_n) for p_n, q_n in zip(p,q)]
    ret = sum(d_1)
    return ret

def get_wires_from_input():

    filepath = Path('input/day_3')
    wires = {}

    with open(filepath) as f:
        for wire, turns in enumerate(f):
            wires[f'wire{wire}'] = [x for x in turns.split(',')]

    return wires

if __name__ == "__main__":
    puzzles_input = get_wires_from_input()
    print(f'Parsed {len(puzzles_input)} wires from input.')
    panel = Panel(coils=puzzles_input)
    print(f'Manhattan dist to closests insection point from origin: {panel.get_closest_intersection_to_point()}')