import unittest
import day_12 as NBodySimul
class Day12_NBody_TestCase(unittest.TestCase):

    # Define a test for happy path using by calling extracted main with actual puzzle input and compare result to verified correct output.
    def test_happypath(self):
        # Correct answers for my particular input
        part1_correct = 8742
        part2_correct = 325433763467176
        self.assertEqual((part1_correct, part2_correct), NBodySimul.main())
if __name__ == "__main__":
    unittest.main()