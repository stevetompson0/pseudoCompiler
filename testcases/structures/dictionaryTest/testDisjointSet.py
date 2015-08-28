import unittest

from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_add(self):
        dset = DisjointSet()
        dset.add("A")
        dset.add("B")
        dset.add("C")
        dset.add("D")
        dset.add("E")

        print(dset)
        print(dset.eleFlags)

    def test_union(self):
        dset = DisjointSet()
        dset.add("A")
        dset.add("B")
        dset.add("C")
        dset.add("D")
        dset.add("E")

        dset.union("A", "B")
        dset.union("B", "C")

        print(dset)
        print(dset.eleFlags)

    def test_find(self):
        dset = DisjointSet()
        dset.add("A")
        dset.add("B")
        dset.add("C")
        dset.add("D")
        dset.add("E")

        dset.union("A", "B")
        dset.union("B", "C")

        print(dset.find("C"))

    def test_reset(self):
        pass

    def test_random(self):
        x = DisjointSet.random()
        print(x)



if __name__ == '__main__':
    unittest.main()
