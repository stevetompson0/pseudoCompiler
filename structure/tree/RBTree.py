'''
Author: Fang Zhou
Date: 2015/6/10
Version: 1.0
Description: red Black Tree data structure, extend from Binary Search Tree. This class use recursively way to implement
RB tree is a self-balancing binary search tree.

Rule:
1. A node is either red or black.
2. The root is black.
3. All leaves (NIL) are black.
4. Every red node must have two black child nodes (and therefore it must have a black parent).
5. Every path from a given node to any of its descendant NIL nodes contains the same number of black nodes.
'''

import glb
from structure.config import *

red = 'R'
black = 'B'

class RBTree(BinarySearchTree):
    __name__ = "RBTree"


    '''
    overwrite BinarySearchTree's function:
    1. add(self,value)
    2. remove(self, value)
    3. random(cls)
    4. clear(self)

    __init__():
    '''

    #initialize a RB tree
    def __init__(self, value=None):
        self._value = value
        self._parent = None
        self._left = None
        self._right = None

        if self._value:
            self._size = 1
            self._nodeFlag = glb.flag_dict['unchanged']
            self._nodeColor = black
        else:
            self._size = 0
            self._nodeFlag = None
            self._nodeColor = None

    @property
    def nodeColor(self):
        return self._nodeColor

    @nodeColor.setter
    def nodeColor(self, nodeColor):
        self._nodeColor = nodeColor

    @property
    def color(self):
        ret = '['
        ret += str(self.nodeColor)

        #to avoid [1[None][None]]
        if self.childrenNo > 0:
            #left subtree
            if self._left:
                ret += str(self._left.color)
            else:
                ret += "[None]"

            #right subtree
            if self._right:
                ret += str(self._right.color)
            else:
                ret += "[None]"
        ret += ']'

        return ret

    def rightRotate(self):
        #todo from visualize.plot import printVar
        #printVar()

        """
        eg. 4[3[2, None], None] -> 3[2,4]
        """
        # print("Rotating " + str(self.val) + ' right, parent ->' + str(self.parent))
        root = self
        pivot = root.left #new root of the balanced tree
        rootVal = root.value
        rootColor = root.nodeColor
        rootFlag = root.nodeFlag#todo flag may not be correct

        #rotate
        root.left = pivot.left
        if pivot.left:
            pivot.left.parent = root
            pivot.left.nodeFlag = glb.flag_dict['visited']

        root.value = pivot.value
        root.nodeColor = pivot.nodeColor
        pivot.value = rootVal
        pivot.nodeColor = rootColor
        root.nodeFlag = pivot.nodeFlag
        pivot.nodeFlag = rootFlag

        pivot.left = pivot.right

        pivot.right = root.right
        if root.right:
            root.right.parent = pivot
        root.right = pivot

    def leftRotate(self):
        #todo from visualize.plot import printVar
        #printVar()

        # print("Rotating " + str(self.val) + ' left, parent ->' + str(self.parent))
        root = self
        pivot = root.right
        rootVal = root.value
        rootColor = root.nodeColor
        rootFlag = root.nodeFlag

        #rotate
        root.right = pivot.right
        if pivot.right:
            pivot.right.parent = root
            pivot.right.nodeFlag = glb.flag_dict['visited']

        #exchange value
        root.value = pivot.value
        pivot.value = rootVal
        root.nodeColor = pivot.nodeColor
        pivot.nodeColor = rootColor
        root.nodeFlag = pivot.nodeFlag
        pivot.nodeFlag = rootFlag

        pivot.right = pivot.left

        pivot.left = root.left
        if pivot.left:
            pivot.left.parent = pivot
        root.left = pivot


    #rebalance the tree after insertion
    def insertion_rebalance(self, newNode):
        '''
        :param value: the value of newly added node, used for finding new node.
        '''

        if newNode is None:
            return

        # newNode = self.find(value) #bug here
        newNode.nodeColor = red #default is red node

        #case 1: root node
        if newNode.parent is None:
            newNode.nodeColor = black

        #case 2: parent is black
        elif newNode.parent.nodeColor == black:
            newNode.nodeColor = red

        else:
            P = newNode.parent #parent node
            G = P.parent #grand parent
            if G.left is P:
                U = G.right #uncle node
            else:
                U = G.left

            #case 3: parent is red and uncle is red
            if U is not None and U.nodeColor == red:
                newNode.nodeColor = red
                P.nodeColor = black
                U.nodeColor = black
                G.nodeColor = red
                self.insertion_rebalance(G)

            #case 4: parent is red, uncle is None or black, parent is G.left
            #todo we only change the value and color of the node, rotation code is in mess
            elif G.left is P:
                if P.right is newNode:
                    P.leftRotate()
                G.rightRotate()
                G.nodeColor = black
                G.right.nodeColor = red

            #case 5: parent is red, uncle is None or black, parent is G.right
            else:
                if P.left is newNode:
                    P.rightRotate()
                G.leftRotate()
                G.nodeColor = black
                G.left.nodeColor = red

    #Add new value to RB tree
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
                    self._left = RBTree(value)
                    self._left._parent = self
                    self._left._nodeFlag = glb.flag_dict['new']
            else:
                if self._right:
                    self._right.add(value)
                else:
                    self._right = RBTree(value)
                    self._right._parent = self
                    self._right._nodeFlag = glb.flag_dict['new']

        self._size += 1

        newNode = self.find(value)
        self.insertion_rebalance(newNode)

    #Remove the matching value in the tree
    def remove(self, value):
        node = self.find(value)

        #if value is found
        if node:
            if node.childrenNo == 2:
                minNode = node.right.find_min()
                node.value = minNode.value
                self.remove_single_child_node(minNode)
            else:
                self.remove_single_child_node(node)

            self._size -= 1


    #Remove the node which has at most one child node
    def remove_single_child_node(self, node):
        P = node.parent #parent
        if node.left:
            C = node.left #single child of node, may be None
        else:
            C = node.right

        #case 1: node is red
        if node.nodeColor == red:
            #simple deletion
            if P.left is node:
                P.left = C
            else:
                P.right = C
            if C:
                C.parent = P

        #case 2: node is black. child is red
        elif node.nodeColor == black and C is not None and C.nodeColor == red:
            node.value = C.value
            node.left = C.left
            node.right = C.right
            if node.left:
                node.left.parent = node
            if node.right:
                node.right.parent = node

        #case 3:node is black, child is black or None
        else:
            #we first replace the node by its child
            # since find_min() return the most left node of the right branch, C must be the right child

            # if C:
            #     node.value = C.value
            #     node.left = C.left
            #     node.right = C.right
            #     if node.left:
            #         node.left.parent = node
            #     if node.right:
            #         node.right.parent = node
            # else:
            #     node.value = None

            if P.left is node:
                P.left = C
                S = P.right # sibling
            else:
                P.right = C
                S = P.left # sibling

            #case 3.1: node is the root
            #In this case, we remove one black node from all paths, done

            #Attention: C and S may be None

            #case 3.X
            #Create a new function to handle this special case and for recursion use
            self.remove_rebalance(C, P, S)

    #rebalance the tree after deletion, especially node is black, child node is black or None
    def remove_rebalance(self, N, P, S):
            #case 4: S is red -> then P must be black
        if S.nodeColor == red:
            if P.right is S:
                P.lrotate()
                P.nodeColor = black
                P.left.nodeColor = red
            else:
                P.rightRotate()
                P.nodeColor = black
                P.right.nodeColor = red

        #case 5: S is black, P is black, SL, SR black/None
        elif S.nodeColor == black and P.nodeColor == black and ((S.left is not None\
            and S.left.nodeColor == black and S.right is not None and S.right.nodeColor == black) or (S.left is None and S.right is None)):
            S.nodeColor = red
            if P.parent is not None:
                #start from case 4 again
                if P.parent.left is P:
                    self.rb_delete_balance(P, P.parent, P.parent.right)
                else:
                    self.rb_delete_balance(P, P.parent, P.parent.left)

        #case 6: S is black, P is red, SL, SR are black/None
        elif S.nodeColor == black and P.nodeColor == red and ((S.left is not None\
            and S.left.nodeColor == black and S.right is not None and S.right.nodeColor == black) or (S.left is None and S.right is None)):
            P.nodeColor = black
            S.nodeColor = red

        #case 7: S is black
        elif S.nodeColor == black:
            #S is P's right child
            if P.right is S:
                if S.left is not None and S.left.nodeColor == red and (S.right is None or S.right.nodeColor == black):
                    S.rightRotate()
                    S.nodeColor = black
                    S.right.nodeColor = red
                P.leftRotate()
                P.right.nodeColor = black
                P.nodeColor = P.left.nodeColor
                P.left.nodeColor = black
            #S is P's left child
            else:
                if S.right is not None and S.right.nodeColor == red and (S.left is None or S.left.nodeColor == black):
                    S.leftRotate()
                    S.nodeColor = black
                    S.left.nodeColor = red
                P.rightRotate()
                P.left.nodeColor = black
                P.nodeColor = P.right.nodeColor
                P.right.nodeColor = black

    #Clear the entire tree
    def clear(self):
        self._value = None
        self._parent = None
        self._left = None
        self._right = None
        self._size = 0
        self._nodeFlag = None
        self._nodeColor = None

    #generate a RB tree randomly
    @classmethod
    def random(cls):
        import random
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), keyNo)

        tree = RBTree()
        for val in randomArr:
            tree.add(val)

        tree.resetFlags()
        return tree

