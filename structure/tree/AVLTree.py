'''
Author: Fang Zhou
Date: 2015/6/9
Version: 1.0
Description: AVL Tree data structure, extend from Binary Search Tree. This class use recursively way to implement AVL Tree
AVL tree is a self-balancing binary search tree.
'''

import glb
from structure.config import *

class AVLTree(BinarySearchTree):
    __name__ = "AVLTree"

    '''
    overwrite BinarySearchTree's function:
    1. add(self,value)
    2. remove(self, value)
    3. random(cls)
    4. clear(self)

    __init__(): add one more field "balancedFactor"
    '''

    #initialize an AVL tree
    def __init__(self, value=None):
        self._value = value
        self._parent = None
        self._left = None
        self._right = None
        self._balanceFactor = 0 #left branch height - right branch height

        if self._value:
            self._size = 1
            self._nodeFlag = glb.flag_dict['unchanged']
        else:
            self._size = 0
            self._nodeFlag = None

    @property
    def balanceFactor(self):
        return self._balanceFactor

    #update balance factor after each insertion or deletion
    def updateBalanceFactor(self):
        if self.value:
            leftHeight = 0
            rightHeight = 0
            if self.left:
                leftHeight = self.left.height
            if self.right:
                rightHeight = self.right.height
            self._balanceFactor = leftHeight - rightHeight
        else:
            self._balanceFactor = 0

    #right rotation
    def rightRotate(self):
        #TODO printvar before rotation

        #[G[P[N][C1]][C2]] -> [P[N][G[C1][C2]]], self is root G
        G = self
        P = G.left #new root of the balanced tree, assert P is not None
        GVal = G.value

        G.value = P.value
        G._nodeFlag = glb.flag_dict['changed']
        G.left = P.left
        if P.left:
            P.left._parent = G
            P.left._nodeFlag = glb.flag_dict['changed']

        P.left = P.right

        P.right = G.right
        if G.right:
            G.right._parent = P

        G.right = P
        P.value = GVal
        P._nodeFlag = glb.flag_dict['changed']


    #left rotation
    def leftRotate(self):
        #TODO printvar before rotation

        #[G[C2][p[C1][N]]
        G = self
        P = G.right#new root of the balanced tree, assert P is not None
        GVal = G.value

        G.value = P.value
        G._nodeFlag = glb.flag_dict['changed']
        G.right = P.right
        if P.right:
            P.right._parent = G
            P.right._nodeFlag = glb.flag_dict['changed']

        P.right = P.left

        P.left = G.left
        if G.left:
            G.left._parent = P

        G.left = P
        P.value = GVal
        P._nodeFlag = glb.flag_dict['changed']


    def rebalance(self, value):
        '''
        rebalance from bottom to top, since all changed balanced factor nodes are on the path from root to new node,
        so we only need to check this path.

        :param value: the value of newly added node, used for finding new node.
        '''

        newNode = self.find(value) #assert newNode is not None

        P = newNode.parent #parent node of new node
        G = None
        if P:
            G = P.parent #grandparent node of new node

        #if P and G exist
        while P and G:
            #left branch high
            if G.balanceFactor > 1:
                #left right case
                if P.balanceFactor < 0:
                    P.leftRotate()
                G.rightRotate()
                #update balance factors after rotations
                self.updateBalanceFactor()
            #right branch high
            elif G.balanceFactor < -1:
                #right left case
                if P.balanceFactor > 0:
                    P.rightRotate()
                G.leftRotate()
                #update balance factors after rotations
                self.updateBalanceFactor()

            #keep looping, possibly up to the root
            P = G
            G = P.parent

            #todo printvar

    #Add new values to AVL Tree, no duplication values allowed
    def add(self, value):
        if self.value == None:
            self.value = value
            self._nodeFlag = glb.flag_dict['new']
        else:
            if self.value == value:
                raise Exception("Value: \"" + str(value) +"\" already exist in tree. Duplication of value is not allowed.")
            #Add to left subtree
            elif self.value > value:
                if self._left:
                    #TODO mark it as tranversed

                    self._left.add(value)
                else:
                    self._left = AVLTree(value)
                    self._left._parent = self
                    self._left._nodeFlag = glb.flag_dict['new']
            else:
                if self._right:
                    self._right.add(value)
                else:
                    self._right = AVLTree(value)
                    self._right._parent = self
                    self._right._nodeFlag = glb.flag_dict['new']

        self._size += 1
        self.updateBalanceFactor()#update balanceFactor after adding new values

        #Attention!!! start rebalance from bottom to top, so we provide the newly added value for finding the new node
        self.rebalance(value)

    #Remove the first occurrence of value in the tree.
    def remove(self, value):
        #call BST remove function
        super().remove(value) #this will decrease tree size by 1
        self.updateBalanceFactor()#update balanceFactor after adding new values

        #todo printvar after BST remove

        #only nodes from root to deleted node will be affected, so we search from the top to bottom
        #to find out the deepest unbalanced node
        unbalancedNode = self.findUnbalancedNode()

        #if the tree is unbalanced
        if unbalancedNode:
            grandNode = None
            if unbalancedNode.balanceFactor < 0:
                if unbalancedNode.right.balanceFactor < 0:
                    grandNode = unbalancedNode.right.right
                else:
                    grandNode = unbalancedNode.right.left
            else:
                if unbalancedNode.left.balanceFactor < 0:
                    grandNode = unbalancedNode.left.right
                else:
                    grandNode = unbalancedNode.left.left
            #need to find the grandNode's value, because rebalance use grandNode for rebalancing
            self.rebalance(grandNode.value)

    #find the deepest unbalanced node, there will be no such a case: two child nodes are unbalanced at the same time
    def findUnbalancedNode(self):
        leftResult = None
        rightResult = None

        if self.left:
            leftResult = self.left.findUnbalancedNode()
        if self.right:
            rightResult = self.right.findUnbalancedNode()

        #at least one of leftResult and rightResult should be None
        if leftResult:
            return leftResult
        elif rightResult:
            return rightResult
        else:
            if self._balanceFactor < -1 or self._balanceFactor > 1:
                return self
            else:
                return None

    #Clear the entire tree
    def clear(self):
        self._value = None
        self._parent = None
        self._left = None
        self._right = None
        self._size = 0
        self._nodeFlag = None
        self._balanceFactor = 0

    #generate a AVL tree randomly
    @classmethod
    def random(cls):
        import random
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), keyNo)

        tree = AVLTree()
        for val in randomArr:
            tree.add(val)

        tree.resetFlags()
        return tree




