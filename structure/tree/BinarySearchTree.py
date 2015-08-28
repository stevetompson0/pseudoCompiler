'''
Author: Fang Zhou
Date: 2015/6/7
Version: 1.0
Description:
A binary search tree (BST), which may sometimes also be called an ordered or
sorted binary tree, is a node-based binary tree data structure which has the
following properties:
1) The left subtree of a node contains only nodes with keys less than the node's key.
2) The right subtree of a node contains only nodes with keys greater than the node's key.
3) Both the left and right subtrees must also be binary search trees.

Currently the tree only designed to accepting numbers
'''

import glb
from structure.config import *

class BinarySearchTree(BinaryTree):

    __name__ = "BinarySearchTree"

    '''
    overwrite BinaryTree's function:
    1. add(self, value)
    2. find(self, value)
    3. remove(self, value)
    4. clear(self)

    New function:
    1. random(cls)

    '''

    #add new values to binary search tree
    def add(self, value):
        if self.value == None:
            self.value = value
            self._nodeFlag = glb.flag_dict['new']
            self._size += 1
        else:
            if self.value == value:
                raise Exception("Value: \"" + str(value) +"\" already exist in tree. Duplication of value is not allowed.")
            #Add to left subtree
            elif self.value > value:
                self._size += 1
                if self._left:
                    #TODO mark it as tranversed

                    self._left.add(value)
                else:
                    self._left = BinarySearchTree(value)
                    self._left._parent = self
                    self._left._nodeFlag = glb.flag_dict['new']
            else:
                self._size += 1
                if self._right:
                    self._right.add(value)
                else:
                    self._right = BinarySearchTree(value)
                    self._right._parent = self
                    self._right._nodeFlag = glb.flag_dict['new']



    #find the subtree whose root value matches "value"
    def find(self, value):
        '''
        :return: root of the subtree, None if not found
        '''
        if self.value == value:
            return self
        elif self.value > value:
            if self.left:
                return self.left.find(value)
            else:
                return None
        else:
            if self.right:
                return self.right.find(value)
            else:
                return None

    #find minimal value in the tree
    def find_min(self):
        if self.left:
            return self.left.find_min()
        else:
            return self


    #remove the first occurrence of value in the tree. (From top to bottom)
    def remove(self, value):
        subtree = self.find(value)

        #if value is found
        if subtree:
            #No child nodes
            if subtree.childrenNo == 0:
                #if parent is not None
                if subtree.parent:
                    #if subtree.parent.value > subtree.value: #this will cause bug such as remove 9 from [9[8][None]]
                    if subtree.parent.left is subtree:
                        subtree.parent.left = None
                    else:
                        subtree.parent.right = None
                #parent is None
                else:
                    subtree.value = None

            #One or more child nodes
            else:
                #right subtree exists
                if subtree.right:
                    minNode = subtree.right.find_min()
                    subtree.value = minNode.value
                    #recursively remove value in subtree
                    minNode.remove(minNode.value)

                #right subtree not exist, left subtree exist
                else:
                    subtree.value = subtree.left.value
                    #recursively remove value in left subtree
                    subtree.left.remove(subtree.left.value)

                    #Method without using recursion
                    # #subtree parent exist
                    # if subtree.parent:
                    #     if subtree.parent.value > subtree.value:
                    #         subtree.parent.left = subtree.left
                    #     else:
                    #         subtree.parent.right = subtree.right
                    # else:
                    #     #can not use: subtree = subtree.left or self = subtree.left
                    #     subtree.value = subtree.left.value
                    #     subtree.left = subtree.left.left
                    #     subtree.right = subtree.left.right

            self._size -= 1

            #TODO mark this node as visited or changed


    #Clear the entire tree
    def clear(self):
        self._value = None
        self._parent = None
        self._left = None
        self._right = None
        self._size = 0
        self._nodeFlag = None

    #generate a BST randomly
    @classmethod
    def random(cls):
        import random
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), keyNo)

        tree = BinarySearchTree()
        for val in randomArr:
            tree.add(val)

        tree.resetFlags()
        return tree