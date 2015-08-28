__author__ = 'zfang6'

import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_init(self):
        a = Array()
        a = [1,2,[3,4]]
        b = Array(a)
        print(b)
        print(b.eleFlags)

    def test_set(self):
        # a = Array([1,2,3,4])
        # a[1] = 9
        # print(a)
        # print(a.eleFlags)

        b = Array([1,2])
        b.append(Array([3,4]))
        b[2][0] = 9
        print(b)
        print(b.eleFlags)

    def test_get(self):
        a = Array([1,2,3,4])
        x = a[0]
        print(a.eleFlags)
        print(x)
        a[0] = 9
        print(a)
        print(a.eleFlags)

    def test_append(self):
        a = Array([1,2,3,4])
        a.append(5)
        print(a)
        print(a.eleFlags)

    def test_insert(self):
        a = Array([1,2,3,4])
        a.insert(1, 9)
        print(a)
        print(a.eleFlags)

    def test_pop(self):
        a = Array([1,2,3,4])
        a.pop()
        print(a)
        print(a.eleFlags)

        a.pop(0)
        print(a)
        print(a.eleFlags)

    def test_remove(self):
        a = Array([1,2,3,4])
        a.remove(3)
        print(a)
        print(a.eleFlags)

    def test_remove(self):
        a = Array([1,2,3,4])
        a.remove(3)
        print(a)
        print(a.eleFlags)

    def test_reverse(self):
        a = Array([1,2,3,4])
        a.append(3)
        a.reverse()
        print(a)
        print(a.eleFlags)

    def test_swap(self):
        a = Array([1,2,3,4])
        a.swap(0,1)
        print(a)
        print(a.eleFlags)

        a.resetFlags()
        print(a.eleFlags)

        a.clear()
        print(a)
        print(a.eleFlags)

    def test_random(self):
        a = Array.random()
        print(a)
        print(a.eleFlags)

    def test_iter(self):
        a = Array([1,2,3,4])
        for b in a:
            print(b)
        print(a.__class__.__name__)


if __name__ == '__main__':
    unittest.main()
