import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_add(self):
        tree = RBTree()
        tree.add(1)
        tree.add(2)
        tree.add(3)
        tree.add(4)


        print(tree)
        print(tree.color)
        print(tree.eleFlags)

    def test_remove(self):
        rbtree = RBTree()
        rbtree.add(1)
        rbtree.add(2)
        rbtree.add(3)
        rbtree.add(4)
        rbtree.add(5)
        rbtree.add(6)
        rbtree.add(7)
        rbtree.add(8)
        rbtree.add(9)
        rbtree.add(10)
        rbtree.add(11)
        rbtree.add(12)
        rbtree.add(13)
        rbtree.add(14)
        rbtree.add(15)
        rbtree.add(16)
        rbtree.add(17)
        rbtree.add(18)
        rbtree.add(19)
        rbtree.add(20)

        print(rbtree)
        print(rbtree.color)
        print(rbtree.size)


        rbtree.remove(16)

        print(rbtree)
        print(rbtree.color)
        print(rbtree.size)


if __name__ == '__main__':
    unittest.main()
