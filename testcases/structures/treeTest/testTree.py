__author__ = 'zfang6'

import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_init(self):
        tree1 = Tree()
        print(tree1)
        print(tree1.size)
        print(tree1.eleFlags)
        print("Height" + str(tree1.height))

        tree1 = Tree(23)
        print(tree1)
        print(tree1.size)
        print(tree1.eleFlags)
        print("Height" + str(tree1.height))

        tree1.value = 4
        print(tree1)
        print(tree1.eleFlags)

        #test reset
        tree1.resetFlags()
        print(tree1.eleFlags)

    def test_random(self):
        tree = Tree.random()
        print(tree)
        print(tree.eleFlags)

        #test clear
        tree.clear()
        print(tree)
        print(tree.eleFlags)


    def test_addChild(self):
        tree = Tree.random()
        tree.addChild(100)
        tree.getChild(0).addChild(9)
        print(tree)
        print(tree.eleFlags)

    def test_findDFS(self):
        tree = Tree.random()
        tree.addChild(100)
        tree.getChild(0).addChild(9)
        print(tree)
        print(tree.eleFlags)
        print("Height: " + str(tree.height))

        print(tree.findDFS(9))
        print(tree)
        print(tree.eleFlags)





if __name__ == '__main__':
    unittest.main()
