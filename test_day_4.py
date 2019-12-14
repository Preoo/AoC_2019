import unittest

class Day4_TestCase(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     pass

    # def setUp(self):
    #     pass

    # def test_Sanity(self):
    #     self.assertTrue(1 == 1, 'failed sanity check. Fix test environment.')

    def test_SixDigit(self):
        from day_4 import filter_six_digits
        #It is a six-digit number 
        valid = 111111
        invalid_short = 11111
        invalid_long = 1111111

        self.assertTrue(filter_six_digits(valid), f'Filtered out a valid 6 digit number')
        self.assertFalse(filter_six_digits(invalid_short), f'Failed to filter invalid number')
        self.assertFalse(filter_six_digits(invalid_long), f'Failed to filter out invalid number')

    def test_AdjacentNumbers(self):
        from day_4 import filter_adjacent_numbers
        #Two adjacent digits are the same (like 22 in 122345)
        valid = 122345
        invalid = 123456

        self.assertTrue(filter_adjacent_numbers(valid), f'Filtered out a valid number')
        self.assertFalse(filter_adjacent_numbers(invalid), f'Failed to filter out invalid number')

    def test_Max2AdjacentNumbers(self):
        from day_4 import filter_two_adjacent_numbers
        #Two adjacent digits are the same (like 22 in 122345)
        valids = (123345, 111122, 112233, 111322)
        invalids = (111123, 123456, 123435, 111111)
        
        for valid in valids:
            self.assertTrue(filter_two_adjacent_numbers(valid), f'Filtered out a valid number {valid}')
        
        for invalid in invalids:
            self.assertFalse(filter_two_adjacent_numbers(invalid), f'Failed to filter out invalid number {invalid}')
        
    def test_NeverDecrease(self):
        from day_4 import filter_never_decrease
        #Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679)
        valid_sim = 111123
        valid_inc = 135679
        invalid = 110123

        self.assertTrue(filter_never_decrease(valid_sim), f'Filtered out a valid number')
        self.assertTrue(filter_never_decrease(valid_inc), f'Filtered out a valid number')
        self.assertFalse(filter_never_decrease(invalid), f'Failed to filter out invalid number')

    def test_compound_filters(self):
        from day_4 import filter_six_digits, filter_adjacent_numbers, filter_never_decrease, combine_filters

        valid = 122345
        invalid = 123456

        #combine all three
        filters = (
            filter_six_digits, filter_adjacent_numbers, filter_never_decrease
            )
        filtered = combine_filters(filters, [valid, invalid])

        self.assertEqual(len(filtered), 1)
        self.assertIn(valid, filtered)
        
if __name__ == "__main__":
    unittest.main()