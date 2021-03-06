import unittest
from day_10 import Asteroid as A

def pretty_print_map(ast_map):
    print('')
    for r in ast_map:
        print(r)
    print('')

class Day10_AsteroidObservatory_TestCase(unittest.TestCase):

    def test_ParseAsteroidMapFromString(self):
        from day_10 import parse_asteroidmap

        _map = \
            [
            '.#..#',
            '.....',
            '#####',
            '....#',
            '...##'
            ]
        _map_string = '\n'.join(_map)
        set_asteroid_locations = {
            A(1,0), A(4,0),
            A(0,2), A(1,2), A(2,2), A(3,2), A(4,2),
            A(4,3),
            A(3,4), A(4, 4)
            }

        self.assertCountEqual(set_asteroid_locations, parse_asteroidmap(_map_string))

    def test_Example_1(self):
        from day_10 import find_optimal_observatory
        _map = \
        [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####'
        ]
        # pretty_print_map(_map)
        #Best is 5,8 with 33 other asteroids detected
        a, c = find_optimal_observatory('\n'.join(_map))
        self.assertEqual(A(5,8), a)
        self.assertEqual(33, c)
        

    def test_Example_2(self):
        from day_10 import find_optimal_observatory
        _map = \
        [
        '#.#...#.#.',
        '.###....#.',
        '.#....#...',
        '##.#.#.#.#',
        '....#.#.#.',
        '.##..###.#',
        '..#...##..',
        '..##....##',
        '......#...',
        '.####.###.'
        ]
        # pretty_print_map(_map)
        #Best is 1,2 with 35 other asteroids detected
        a, c = find_optimal_observatory('\n'.join(_map))
        self.assertEqual(A(1,2), a)
        self.assertEqual(35, c)
        

    def test_Example_3(self):
        from day_10 import find_optimal_observatory
        _map = \
        [
        '.#..#..###',
        '####.###.#',
        '....###.#.',
        '..###.##.#',
        '##.##.#.#.',
        '....###..#',
        '..#.#..#.#',
        '#..#.#.###',
        '.##...##.#',
        '.....#.#..'
        ]
        # pretty_print_map(_map)
        #Best is 6,3 with 41 other asteroids detected
        a, c = find_optimal_observatory('\n'.join(_map))
        self.assertEqual(A(6,3), a)
        self.assertEqual(41, c)
        

    def test_Example_4(self):
        from day_10 import find_optimal_observatory
        _map = \
        [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##'
        ]
        # pretty_print_map(_map)
        #Best is 11,13 with 210 other asteroids detected
        a, c = find_optimal_observatory('\n'.join(_map))
        self.assertEqual(A(11,13), a)
        self.assertEqual(210, c)
        
    def test_LaserWipeout(self):
        from day_10 import find_optimal_observatory, evaporate_asteroid_field
        _map = \
        [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##'
        ]
        a, _ = find_optimal_observatory('\n'.join(_map))
        evaporation_order_list = evaporate_asteroid_field('\n'.join(_map), a)
        self.assertEqual(299, len(evaporation_order_list))
        print(evaporation_order_list[-1])
        print(evaporation_order_list[200 - 1])

if __name__ == "__main__":
    unittest.main()