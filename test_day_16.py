import unittest
import day_16 as fft

class Day16_FlawedFrequencyTransmission_TestCase(unittest.TestCase):
    def test_pattern_generation(self):
        sig = [1,2,3,4,5,6,7,8]
        base_pttr = [0, 1, 0, -1]
        expected_pattern = [0,1,1,0,0,-1,-1,0]
        # expected_pattern = [0,0,0,1,1,1,1,0]
        nth_elem = 2
        r = fft.generate_pattern_for_element(base_pttr, nth_elem, len(sig))
        self.assertEqual(expected_pattern, list(r)) # testing if returning a numpy array helps with large inputs

    def test_short_example(self):
        sig = [1,2,3,4,5,6,7,8]
        expected = [0,1,0,2,9,4,9,8]
        phases = 4
        self.assertEqual(expected, fft.FFT(sig, phases=phases))
    
    def test_long_example_1(self):
        sig = [int(d) for d in '80871224585914546619083218645595']
        expected = [int(d) for d in '24176176']
        self.assertEqual(expected, fft.FFT(sig, phases=100)[:8])

    def test_long_example_2(self):
        sig = [int(d) for d in '19617804207202209144916044189917']
        expected = [int(d) for d in '73745418']
        self.assertEqual(expected, fft.FFT(sig, phases=100)[:8])

    def test_long_example_3(self):
        sig = [int(d) for d in '69317163492948606335995924319873']
        expected = [int(d) for d in '52432133']
        self.assertEqual(expected, fft.FFT(sig, phases=100)[:8])

    def test_long_example_str_in(self):
        sig = '69317163492948606335995924319873'
        expected = [int(d) for d in '52432133']
        self.assertEqual(expected, fft.FFT(sig, phases=100)[:8])

if __name__ == "__main__":
    unittest.main()