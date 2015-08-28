__author__ = 'zfang6'

import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):

    def test_init(self):
        matrix = StringMatrix.random()
        print(matrix)
        matrix.addEdge(0,0,1,1)
        print(matrix.eleFlags)
        print(matrix.edges)
        matrix[0][0] = "fa"
        print(matrix.eleFlags)




if __name__ == '__main__':
    unittest.main()
