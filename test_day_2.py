import unittest

class Day1_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_Sanity(self):
        self.assertTrue(1 == 1, 'failed sanity check. Fix test environment.')
        
if __name__ == "__main__":
    unittest.main()