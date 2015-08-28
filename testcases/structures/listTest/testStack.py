__author__ = 'zfang6'

import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = Stack()
        a.push(1)
        a.push(2)
        a.push(4)
        print(a.length)
        print(a.top)


if __name__ == '__main__':
    unittest.main()
