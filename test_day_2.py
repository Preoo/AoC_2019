import unittest

class Day2_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_Sanity(self):
        self.assertTrue(1 == 1, 'failed sanity check. Fix test environment.')

    def test_example1(self):
        import day_2 as machine
        program = [1,9,10,3,2,3,11,0,99,30,40,50]
        expected = [3500,9,10,70,2,3,11,0,99,30,40,50]
        self.assertEqual(expected, machine.run(program), f'Example 1 failed to produce proper output')
        
    def test_example2(self):
        import day_2 as machine
        program = [1,0,0,0,99]
        expected = [2,0,0,0,99]
        self.assertEqual(expected, machine.run(program), f'Example 2 failed to produce proper output')

    def test_example3(self):
        import day_2 as machine
        program = [2,3,0,3,99]
        expected = [2,3,0,6,99]
        self.assertEqual(expected, machine.run(program), f'Example 3 failed to produce proper output')

    def test_example4(self):
        import day_2 as machine
        program = [2,4,4,5,99,0]
        expected = [2,4,4,5,99,9801]
        self.assertEqual(expected, machine.run(program), f'Example 4 failed to produce proper output')

    def test_example5(self):
        import day_2 as machine
        program = [1,1,1,4,99,5,6,0,99]
        expected = [30,1,1,4,2,5,6,0,99]
        self.assertEqual(expected, machine.run(program), f'Example 5 failed to produce proper output')

if __name__ == "__main__":
    unittest.main()