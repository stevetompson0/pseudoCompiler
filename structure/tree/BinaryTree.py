'''
Author: Fang Zhou
Date: 2015/6/1
Version: 1.0
Description: Binary Tree, this is just an abstract class.
'''

import glb

class BinaryTree():
    __name__ = "BinaryTree"

    '''
    property:
    1. value
    2. left
    3. right
    4. parent
    5. childrenNo
    6. size
    7. height
    8. eleFlags


    setter:
    1. value
    2. left
    3. right
    '''

    #initialize a binary tree
    def __init__(self, value=None):
        self._value = value
        self._parent = None
        self._left = None
        self._right = None

        if self._value:
            self._size = 1
            self._nodeFlag = glb.flag_dict['unchanged']
        else:
            self._size = 0
            self._nodeFlag = None

    @property
    def value(self):
        return self._value

    #set value of tree node
    @value.setter
    def value(self, value):
        self._value = value

    @property
    def nodeFlag(self):
        return self._nodeFlag

    @nodeFlag.setter
    def nodeFlag(self, nodeFlag):
        self._nodeFlag = nodeFlag

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    #number of child nodes
    @property
    def childrenNo(self):
        count = 0
        if self._left:
            count += 1
        if self._right:
            count += 1
        return count


    #return size of the tree
    @property
    def size(self):
        return self._size

    #return tree height
    @property
    def height(self):
        leftHeight = 0
        rightHeight = 0

        if self._left:
            leftHeight = self._left.height
        if self._right:
            rightHeight = self._right.height

        maxHeight = max(leftHeight, rightHeight)

        if self._value:
            return maxHeight + 1
        else:
            #empty tree
            return 0

    #pre-order representation
    @property
    def eleFlags(self):
        ret = '['
        ret += str(self._nodeFlag)

        #to avoid [1[None][None]]
        if self.childrenNo > 0:
            #left subtree
            if self._left:
                ret += str(self._left.eleFlags)
            else:
                ret += "[None]"

            #right subtree
            if self._right:
                ret += str(self._right.eleFlags)
            else:
                ret += "[None]"
        ret += ']'

        return ret

    #reset all the element flags
    def resetFlags(self):
        self._nodeFlag = glb.flag_dict['unchanged']
        if self._left:
            self._left.resetFlags()
        if self._right:
            self._right.resetFlags()

    #to string, pre-order representation
    def __str__(self):
        ret = '['
        ret += str(self.value)

        #to avoid [1[None][None]]
        if self.childrenNo > 0:
            #left subtree
            if self._left:
                ret += str(self._left)
            else:
                ret += "[None]"

            #right subtree
            if self._right:
                ret += str(self._right)
            else:
                ret += "[None]"
        ret += ']'

        return ret



    #add child node
    def add(self, value):
        pass

    #find value
    def find(self, value):
        pass

    #remove
    def remove(self, value):
        pass

    #random()


