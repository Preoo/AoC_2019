import unittest
from Shared.IntCodeMachine import machine as machine

class Day2_Regression_TestCase(unittest.TestCase):

    def test_example1(self):
        
        program = [1,9,10,3,2,3,11,0,99,30,40,50]
        expected = [3500,9,10,70,2,3,11,0,99,30,40,50]
        self.assertEqual(expected, machine.run(program), f'Example 1 failed to produce proper output')
        
    def test_example2(self):
        
        program = [1,0,0,0,99]
        expected = [2,0,0,0,99]
        self.assertEqual(expected, machine.run(program), f'Example 2 failed to produce proper output')

    def test_example3(self):
        
        program = [2,3,0,3,99]
        expected = [2,3,0,6,99]
        self.assertEqual(expected, machine.run(program), f'Example 3 failed to produce proper output')

    def test_example4(self):
        
        program = [2,4,4,5,99,0]
        expected = [2,4,4,5,99,9801]
        self.assertEqual(expected, machine.run(program), f'Example 4 failed to produce proper output')

    def test_example5(self):
        
        program = [1,1,1,4,99,5,6,0,99]
        expected = [30,1,1,4,2,5,6,0,99]
        self.assertEqual(expected, machine.run(program), f'Example 5 failed to produce proper output')

class Day5_Regression_TestCase(unittest.TestCase):

    def test_MultWithParamaterMode(self):
        
        program = [1002,4,3,4,33]
        output = [1002,4,3,4,99]
        self.assertEqual(output, machine.run(program), f'Incorrect execution of mult with immidiate mode params')
        
    def test_AddWithNegativeNumbers(self):
        program = [1101,100,-1,4,0]
        output = [1101,100,-1,4,99]
        self.assertEqual(output, machine.run(program), f'Incorrect execution of add negative with immidiate mode params')

    def test_IO_Instructions(self):
        program = [3,0,4,0,99]
        inputs = [123]
        outputs = []
        machine.run(program, inputs=inputs, outputs=outputs) #take inputs and appends to outputs?
        self.assertEqual(inputs, outputs, f'Program should have returned output equal to input')

    """ These tests are combined in following test
    def test_EQ_Instructions(self):
        #in position mode

        #in immediate mode
        pass

    def test_LE_Instruction(self):
        #in position mode

        #in immediate mode
        pass
    def test_JMP_Instructions(self):
        pass

    """

    def test_InputIsLessEqualGreater_than_8(self):
        program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        
        #less than 8
        in_io = [-1]
        io_out = []
        machine.run(program.copy(), inputs=in_io, outputs=io_out)
        self.assertEqual(io_out, [999])
        #equals to 8
        in_io = [8]
        io_out.clear()
        machine.run(program.copy(), inputs=in_io, outputs=io_out)
        self.assertEqual(io_out, [1000])
        #greater than 8
        in_io = [22]
        io_out.clear()
        machine.run(program.copy(), inputs=in_io, outputs=io_out)
        self.assertEqual(io_out, [1001])
        

if __name__ == "__main__":
    unittest.main()