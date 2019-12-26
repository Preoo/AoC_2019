import unittest
from day_5 import IntCodeMachine

class Day9_IntCodeMachineRelativeMode_TestCase(unittest.TestCase):

    def test_Quine(self):
        program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        m = IntCodeMachine(program.copy(), memory=100)
        for _ in m.run():
            pass

        self.assertEqual(program, list(m.io_o))

    def test_Outputs16digitsLong(self):
        def digits(number):
            return len(str(number))
        m = IntCodeMachine([1102,34915192,34915192,7,4,7,99,0], memory=100)
        for _ in m.run():
            pass
        
        self.assertEqual(16, digits(m.out_latest()))

    def test_LargeValues(self):
        m = IntCodeMachine([104,1125899906842624,99])
        for _ in m.run():
            pass
        
        self.assertEqual(1125899906842624, m.out_latest())

if __name__ == "__main__":
    unittest.main()