import unittest
from utils.recursive import get_block_count
from utils.consoleManager import stdoutIO

class MyTestCase(unittest.TestCase):
    def test_count(self):
        with open("sampleCode", 'r') as file:
            content = ''.join(file.readlines()).split('\n')
        print(get_block_count(content, 22))

    def test_recursive(self):
        from pseudo import pseudo
        pseudo("sampleCode")


    def test_print(self):
        code = "print(9)"
        with stdoutIO() as s:
            exec(code)
        # print(s.getvalue())
        print(9)

if __name__ == '__main__':
    unittest.main()
