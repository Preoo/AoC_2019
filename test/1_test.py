import unittest

class Day1_TestCase(unittest.TestCase):

    def test_default(self):
        self.assertTrue(True, 'Unittests are not running')

    def testAdd(self):
        self.assertEqual(1+2, 3, 'Sanity')

if __name__ == "__main__":
    unittest.main()