from Shared.IntCodeMachine.machine import IntCodeMachine
from collections import deque
from collections import namedtuple
from collections import defaultdict
import numpy as np

class Robot:
    Pos = namedtuple('Pos', ['x', 'y'])
    def __init__(self, program, memory=10000, panel=None):
    
        self._cpu = IntCodeMachine(program.copy(), memory=memory)
        self._panel = panel if panel else Panel()
        self.pos = self.Pos(x=0, y=0)
        self.direction = 'up'
        self.step = 1
        
        self.move = {
            'up' : lambda pos : self.Pos(pos.x, pos.y + self.step),
            'down' : lambda pos : self.Pos(pos.x, pos.y - self.step),
            'left' : lambda pos : self.Pos(pos.x - self.step, pos.y),
            'right' : lambda pos : self.Pos(pos.x + self.step, pos.y)
        }

        self.turn = {
            'up' : lambda direction : 'left' if direction == 'left' else 'right',
            'down' : lambda direction : 'right' if direction == 'left' else 'left',
            'left' : lambda direction : 'down' if direction == 'left' else 'up',
            'right' : lambda direction : 'up' if direction == 'left' else 'down'
        }
        self.steer = {
            0 : 'left',
            1 : 'right'
        }
        self.sprite = {
            'up' : '^',
            'down' : 'v',
            'left' : '<',
            'right' : '>' 
        }

    def turn_and_move(self, command):
        self._panel.tracks.append(self.pos)
        turn_direction = self.steer[command]
        self.direction = self.turn[self.direction](turn_direction)
        self.pos = self.move[self.direction](self.pos)

    def paint(self, pos, color):
        self._panel.set_panel_color((pos.x, pos.y), color)

    def run(self):
        #_iter_cpu = iter(self._cpu)
        while not self._cpu.halted:
            #get colors from panel, self._cpu.feed_input([color])
            cur_pos = (self.pos.x, self.pos.y)
            self._cpu.feed_inputs([self._panel.get_panel_color(cur_pos)])

            try:
                for _ in self._cpu.run():
                    pass
            except StopIteration:
                continue
            
            #get outputs and paint, rotate and move bot
            #don't paint the panel bot halts on
            if not self._cpu.halted:
                paint_color = self._cpu.out()
                turn_direction = self._cpu.out()

                self.paint(self.pos, paint_color)
                self.turn_and_move(turn_direction)
        
        #return

class Panel:
    def __init__(self):
        # A better option would have been to have panel own robot
        # if task required to display robots position and orientation
        self.painted_tiles = defaultdict(int)
        self.tracks = []   #record movement of robot
        self.paints = {
            0 : ' ',    #black
            1 : '*'     #white
        }

    def get_panel_color(self, at_pos):
        return self.painted_tiles[at_pos]
    
    def set_panel_color(self, at_pos, color):
        self.painted_tiles[at_pos] = color

    def show_hull(self):
        # Figure out how large hull needs to be to contain all panels
        half_width, half_height = 1, 1
        for pos in self.painted_tiles.keys():
            x, y = pos
            if abs(x) > half_width:
                half_width = abs(x)
            if abs(y) > half_height:
                half_height = abs(y)

        #width: half_width, height: half_width * 2
        # shape = (rows, columns)
        hull = np.zeros((half_width + 1, half_height * 2 + 1), dtype=int)

        for pos, color in self.painted_tiles.items():
            x, y = pos
            hull[x][y + half_height] = color
        
        for line in hull:
            for c in line:
                print(self.paints[c], end='')
            print('')

def main():

    painting_robot = [3,8,1005,8,319,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,28,2,1008,7,10,2,4,17,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,59,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,81,1006,0,24,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,105,2,6,13,10,1006,0,5,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,134,2,1007,0,10,2,1102,20,10,2,1106,4,10,1,3,1,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,172,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,194,1,103,7,10,1006,0,3,1,4,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,228,2,109,0,10,1,101,17,10,1006,0,79,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,260,2,1008,16,10,1,1105,20,10,1,3,17,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,295,1,1002,16,10,101,1,9,9,1007,9,1081,10,1005,10,15,99,109,641,104,0,104,1,21101,387365733012,0,1,21102,1,336,0,1105,1,440,21102,937263735552,1,1,21101,0,347,0,1106,0,440,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,3451034715,1,1,21101,0,394,0,1105,1,440,21102,3224595675,1,1,21101,0,405,0,1106,0,440,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,838337454440,1,21102,428,1,0,1105,1,440,21101,0,825460798308,1,21101,439,0,0,1105,1,440,99,109,2,22101,0,-1,1,21102,1,40,2,21101,0,471,3,21101,461,0,0,1106,0,504,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,466,467,482,4,0,1001,466,1,466,108,4,466,10,1006,10,498,1102,1,0,466,109,-2,2105,1,0,0,109,4,2101,0,-1,503,1207,-3,0,10,1006,10,521,21101,0,0,-3,21202,-3,1,1,22102,1,-2,2,21101,1,0,3,21102,540,1,0,1105,1,545,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,568,2207,-4,-2,10,1006,10,568,22102,1,-4,-4,1106,0,636,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,587,1,0,1105,1,545,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,606,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,628,22102,1,-1,1,21102,1,628,0,105,1,503,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

    surface_panel = Panel()
    bot = Robot(painting_robot, panel=surface_panel)

    bot.run()
    
    #Part 1
    newly_painted_tiles = set(surface_panel.painted_tiles.keys())

    print(f'Robot painted over {len(newly_painted_tiles)} tiles.')

    #Part 2

    surface_panel = Panel()
    bot = Robot(painting_robot, panel=surface_panel)
    surface_panel.set_panel_color((0,0), 1)
    bot.run()
    
    surface_panel.show_hull()

    # For tests
    return len(newly_painted_tiles)

if __name__ == "__main__":
    main()