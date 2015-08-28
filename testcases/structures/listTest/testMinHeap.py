import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):

    def test_init(self):
        l = [3,2,1]
        heap = BinaryMinHeap(l)
        print(heap)
        print(heap.eleFlags)



    def test_push(self):
        heap = BinaryMinHeap()
        heap.push(5)
        heap.push(4)
        heap.push(3)
        heap.push(2)
        heap.push(1)
        print(heap)
        print(heap.elements)
        print(heap.eleFlags)
        print(heap.length)
        print(heap.top)
        print(heap.isEmpty)
        print(len(heap))


    def test_iter(self):
        heap = BinaryMinHeap()
        heap.push(5)
        heap.push(4)
        heap.push(3)
        heap.push(2)
        heap.push(1)
        for ele in heap:
            print(ele)

    def test_pop(self):
        heap = BinaryMinHeap()
        heap.push(5)
        heap.push(4)
        heap.push(3)
        heap.push(2)
        heap.push(1)
        print(heap.pop())
        print(heap)
        print(heap.eleFlags)

    def test_clear(self):
        #test reset clear
        heap = BinaryMinHeap()
        heap.push(5)
        heap.push(4)
        heap.push(3)
        heap.push(2)
        heap.push(1)

        heap.resetFlags()
        print(heap.eleFlags)

        heap.clear()
        print(heap)
        print(heap.eleFlags)



    def test_random(self):
        heap = BinaryMinHeap.random()
        print(heap)

if __name__ == '__main__':
    unittest.main()
