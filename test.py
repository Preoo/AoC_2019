import unittest

class Day1_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_Examples(self):
        import day_1 as d1
        self.assertEqual(d1.calc_fuel([2]), 0, 'Failed round down.')
        self.assertEqual(d1.calc_fuel([12]), 2, 'Failed to calculate correct amount for single module weight.')
        self.assertEqual(d1.calc_fuel([14]), 2, 'Failed to calculate correct amount for single module weight.')
        self.assertEqual(d1.calc_fuel([1969]), 654, 'Failed to calculate correct amount for single module weight.')
        self.assertEqual(d1.calc_fuel([100756]), 33583, 'Failed to calculate correct amount for single module weight.')

    def test_ListOfExamples(self):
        import day_1 as d1
        self.assertEqual(d1.calc_fuel([12,14]), 4, 'Failed to calculate correct amount for list of module weights.')
        self.assertEqual(d1.calc_fuel([14,1969]), 656, 'Failed to calculate correct amount for list of module weights.')

    def test_ReadInput(self):
        import day_1 as d1
        expected_count:int = 6
        dummy_input = \
            """
            94697
            83282
            74533
            68418
            145578
            59032

            """
        read_count = sum(1 for x in d1.get_input_from_str(dummy_input))
        self.assertEqual(expected_count, read_count, 'Failed to parse dummy input')

    def test_ReadInputFile(self):
        import day_1 as d1
        from pathlib import Path
        expected_count:int = 100
        filepath = Path('input/day_1')
        read_count = sum(1 for x in d1.get_input_from_file(filepath))
        self.assertEqual(expected_count, read_count, f'Failed to parse input from file {filepath.name}')

    def test_ReadInputAndCalc(self):
        import day_1 as d1
        test = \
            """
            12
            14

            """
        expected = 4
        result = d1.calc_fuel(d1.get_input_from_str(test))

        self.assertEqual(result, expected, f'Failed to calculate fuel from input string')

    def test_Examples_Part2(self):
        """
        A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
        At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
        The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
        """
        import day_1 as d1
        self.assertEqual(d1.calc_fuel([14]) + d1.calc_fuel_for_fuel(2), 2, 'Failed to calculate correct amount for single module weight + fuel.')
        self.assertEqual(d1.calc_fuel([1969]) + d1.calc_fuel_for_fuel(654), 966, 'Failed to calculate correct amount for single module weight + fuel.')
        self.assertEqual(d1.calc_fuel([100756]) + d1.calc_fuel_for_fuel(33583), 50346, 'Failed to calculate correct amount for single module weight + fuel.')
        self.assertEqual(d1.calc_fuel_for_fuel(100756), 50346, 'Failed to calculate correct amount for single module weight + fuel.')
        
if __name__ == "__main__":
    unittest.main()