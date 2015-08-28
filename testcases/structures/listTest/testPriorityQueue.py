import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_MinPriorityQueue_Add(self):
        minQ = MinPriorityQueue()
        minQ.add_with_priority("A",9)
        minQ.add_with_priority("B",4)
        minQ.add_with_priority("C",6)
        minQ.add_with_priority("D",2)
        minQ.add_with_priority("E",1)

        print(minQ)
        print(minQ.eleFlags)


        x = minQ.extract_min()
        print(x)
        print(minQ)
        print(minQ.eleFlags)



    def test_MinPriorityQueue_Decrease(self):
        minQ = MinPriorityQueue()
        minQ.add_with_priority("A",9)
        minQ.add_with_priority("B",4)
        minQ.add_with_priority("C",6)
        minQ.add_with_priority("D",2)
        minQ.add_with_priority("E",1)

        print(minQ)
        print(minQ.eleFlags)

        minQ.change_priority("A", 0)
        print(minQ)
        print(minQ.eleFlags)


    def test_MaxPriorityQueue_Add(self):
        maxQ = MaxPriorityQueue()
        maxQ.add_with_priority("A",9)
        maxQ.add_with_priority("B",4)
        maxQ.add_with_priority("C",6)
        maxQ.add_with_priority("D",2)
        maxQ.add_with_priority("E",1)

        print(maxQ)
        print(maxQ.eleFlags)


        x = maxQ.extract_max()
        print(x)
        print(maxQ)
        print(maxQ.eleFlags)



    def test_MaxPriorityQueue_Decrease(self):
        maxQ = MaxPriorityQueue()
        maxQ.add_with_priority("A",9)
        maxQ.add_with_priority("B",4)
        maxQ.add_with_priority("C",6)
        maxQ.add_with_priority("D",2)
        maxQ.add_with_priority("E",1)

        print(maxQ)
        print(maxQ.eleFlags)

        maxQ.change_priority("A", 0)
        print(maxQ)
        print(maxQ.eleFlags)

        maxQ.resetFlags()
        print(maxQ.eleFlags)

    def test_random(self):
        a = MinPriorityQueue.random()
        print(a)
        print(a.eleFlags)

        b = MaxPriorityQueue.random()
        print(b)
        print(b.eleFlags)


if __name__ == '__main__':
    unittest.main()
