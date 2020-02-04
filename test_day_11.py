import unittest
import day_11 as HullPainter
class Day11_SpacePolice_TestCase(unittest.TestCase):

    # Define a test for happy path using by calling extracted main with actual puzzle input and compare result to verified correct output.
    def test_happypath(self):
        #for my puzzle input, correct answer was 2293 for part 1. Part 2 will remain untested as it is annoying and relies on same functionality.
        self.assertEqual(2293, HullPainter.main())

if __name__ == "__main__":
    unittest.main()