import unittest
import day_7 as AmpController
class Day7_AmplifierControllerChaining_TestCase(unittest.TestCase):

    # Define a test for happy path using by calling extracted main with actual puzzle input and compare result to verified correct output.
    def test_happypath(self):
        # Correct answers:
        #   Part 1: Max thruster signal is 844468
        #   Part 2: Max thruster signal is 4215746
        self.assertEqual((844468, 4215746), AmpController.main())

if __name__ == "__main__":
    unittest.main()