import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):
    def test_add(self):
        tree = AVLTree()
        tree.add(1)
        tree.add(3)
        tree.add(2)
        tree.add(4)
        print(tree)
        print(tree.eleFlags)

    def test_remove(self):
        tree = AVLTree()
        tree.add(1)
        tree.add(11)
        tree.add(6)
        tree.add(8)
        tree.add(20)
        tree.add(7)
        tree.add(9)
        tree.add(10)
        tree.add(15)
        tree.add(12)

        print(tree)

        tree.remove(11)
        tree.remove(1)
        print(tree)

        tree.remove(7)
        print(tree)
        print(tree.size)
        print(tree.eleFlags)

    def test_random(self):
        tree = AVLTree.random()
        print(tree)
        print(tree.eleFlags)



if __name__ == '__main__':
    unittest.main()
