import unittest

class Day3_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_Sanity(self):
        self.assertTrue(1 == 1, 'failed sanity check. Fix test environment.')

    def test_ManhattanDistance(self):
        from day_3 import manhattan_distance
        p = [1, 2]
        q = [0, 1]
        expected_result = 2
        self.assertEqual(expected_result, manhattan_distance(p,q), 'manhattan distance returned incorrect value.')

        p = [1, 2]
        q = [0, -2]
        expected_result = 5
        self.assertEqual(expected_result, manhattan_distance(p,q), 'manhattan distance returned incorrect value.')

    def test_WireStep(self):
        from day_3 import Wire
        moves = ['U1', 'R01', 'D1', 'L1']
        expected_endpos = (0,0)
        expected_steps = [(0,0), (0,1), (1,1), (1,0), (0,0)]
        wire = Wire('test')
        wire.lay(moves)
        self.assertEqual(expected_steps, wire.steps, f'Wire has incorrect steps')
        self.assertEqual(expected_endpos, wire.steps[-1], f'Wire has invalid end position')

    def test_PanelHasCorrectWires(self):
        from day_3 import Panel, Wire
        wires = {
            'wire0' : ['U1', 'U1'],
            'wire1' : ['D1', 'D2']
        }
        valid_endpoints = [(0,2),(0,-3)]
        panel = Panel(coils=wires)

        self.assertTrue(len(wires) == len(panel.wires), f'Panel does not contain correct number of wires')

        for wire, endpoint in zip(panel.wires, valid_endpoints):
            hasName = wire.name in wires
            self.assertTrue(hasName, f'Wire is not in Panel')
            self.assertEqual(endpoint, wire.steps[-1], f'Wire is a mess')


    def test_WireCrossDistance_1(self):
        from day_3 import Panel, Wire
        wire0 = [x for x in "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')]
        wire1 = [x for x in "U62,R66,U55,R34,D71,R55,D58,R83".split(',')]
        expected = 159

        panel = Panel(coils={'wire0' : wire0, 'wire1' : wire1})
        closest = panel.get_closest_intersection_to_point()
        self.assertEqual(expected, closest)

    def test_WireCrossDistance_2(self):
        from day_3 import Panel, Wire
        wire0 = [x for x in "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(',')]
        wire1 = [x for x in "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')]
        expected = 135

        panel = Panel(coils={'wire0' : wire0, 'wire1' : wire1})
        closest = panel.get_closest_intersection_to_point()
        self.assertEqual(expected, closest)

    def test_WireLeastSteps_1(self):
        from day_3 import Panel, Wire
        wire0 = [x for x in "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')]
        wire1 = [x for x in "U62,R66,U55,R34,D71,R55,D58,R83".split(',')]
        expected = 610

        panel = Panel(coils={'wire0' : wire0, 'wire1' : wire1})
        least_steps = panel.get_least_steps_to_intersection()
        self.assertEqual(expected, least_steps)

    def test_WireLeastSteps_2(self):
        from day_3 import Panel, Wire
        wire0 = [x for x in "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(',')]
        wire1 = [x for x in "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')]
        expected = 410

        panel = Panel(coils={'wire0' : wire0, 'wire1' : wire1})
        least_steps = panel.get_least_steps_to_intersection()
        self.assertEqual(expected, least_steps)
        
if __name__ == "__main__":
    unittest.main()