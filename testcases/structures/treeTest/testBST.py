import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):
    def test_init(self):
        tree = BinarySearchTree()
        tree.add(1)
        tree.add(2)
        tree.add(3)
        tree.add(4)
        self.assertEqual(str(tree), "[1[None][2[None][3[None][4]]]]")
        self.assertEqual(tree.eleFlags, "[1[None][1[None][1[None][1]]]]")

        #test left
        self.assertEqual(tree.left, None)
        #test right
        self.assertEqual(str(tree.right), "[2[None][3[None][4]]]")
        #test parent
        self.assertEqual(str(tree.right.parent), "[1[None][2[None][3[None][4]]]]")
        #test childrenNo
        self.assertEqual(tree.childrenNo, 1)
        #test size
        self.assertEqual(tree.size, 4)
        #test height
        self.assertEqual(tree.height, 4)
        #test resetFlags
        tree.resetFlags()
        self.assertEqual(tree.eleFlags, "[0[None][0[None][0[None][0]]]]")

    def test_find(self):
        tree = BinarySearchTree()
        tree.add(9)
        tree.add(6)
        tree.add(7)
        tree.add(2)
        tree.add(4)
        print(tree)
        subtree = tree.find(6)
        self.assertEqual(str(subtree), "[6[2[None][4]][7]]")
        self.assertEqual(str(subtree.parent), "[9[6[2[None][4]][7]][None]]")
        self.assertEqual(subtree.size, 4)

    def test_delete_case1(self):
        #no child nodes
        tree = BinarySearchTree()
        tree.add(1)
        tree.remove(1)
        self.assertEqual(str(tree), "[None]")
        self.assertEqual(tree.size, 0)


    def test_delete_case2(self):
        #right subtree exist
        tree = BinarySearchTree()
        tree.add(9)
        tree.add(6)
        tree.add(7)
        tree.add(2)
        tree.add(4)

        tree.remove(6)
        self.assertEqual(str(tree), "[9[7[2[None][4]][None]][None]]")
        self.assertEqual(tree.size, 4)
        print(tree.left)
        print(tree.left.left)
        print(tree.left.left.parent)

    def test_delete_case3(self):
        #right subtree exist, min node has children
        tree = BinarySearchTree()
        tree.add(9)
        tree.add(3)
        tree.add(1)
        tree.add(6)
        tree.add(4)
        tree.add(5)
        tree.remove(3)

        self.assertEqual(str(tree), "[9[4[1][6[5][None]]][None]]")
        self.assertEqual(tree.size, 5)

    def test_delete_case4(self):
        tree = BinarySearchTree()
        tree.add(9)
        tree.add(8)
        tree.add(7)
        tree.add(6)
        tree.add(5)

        tree.remove(9)
        print(tree)

        self.assertEqual(tree.size, 4)

    def test_random(self):
        tree = BinarySearchTree.random()
        print(tree)







if __name__ == '__main__':
    unittest.main()
