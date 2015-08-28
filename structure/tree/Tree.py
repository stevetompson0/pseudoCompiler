
'''
Author: Fang Zhou
Date: 2015/5/29
Version: 1.0
Description: Tree data structure.

A tree can be defined recursively (locally) as a collection of nodes (starting at a root node),
where each node is a data structure consisting of a value, together with a list of nodes (the "children"),
with the constraints that no node is duplicated. A tree can be defined abstractly as a whole (globally)
as an ordered tree, with a value assigned to each node.
'''


import glb

class Tree():
    __name__ = "Tree"

    #initialize an tree
    def __init__(self, value=None):
        self._value = value
        self._children = []
        self._parent = None
        if self.value:
            self._size = 1
            self._nodeFlag = glb.flag_dict['unchanged']
        else:
            self._size = 0
            self._nodeFlag = None


    #get value of tree root
    @property
    def value(self):
        # #if the root node is not empty, set flag to visited
        # if self._value != None:
        #     self._nodeFlag = glb.flag_dict['visited']
        return self._value

    #set the value of tree root
    @value.setter
    def value(self, value):
        #if root value is None, add size by 1
        if self.size == 0:
            self.size += 1

        self._value = value
        self._nodeFlag = glb.flag_dict['changed']

    #get the number of child nodes
    @property
    def childrenNo(self):
        return len(self._children)

    @property
    def size(self):
        return self._size

    @property
    def height(self):
        maxHeight = 0
        for subtree in self._children:
            if subtree.height > maxHeight:
                maxHeight = subtree.height

        if self._value:
            return maxHeight + 1
        else:
            #emtpy tree
            return 0

    @property
    def eleFlags(self):
        ret = '['
        ret += str(self._nodeFlag)

        for subtree in self._children:
            ret += str(subtree.eleFlags)

        ret += ']'
        return ret


    #clear
    def clear(self):
        self._value = None
        self._children = []
        self._parent = None
        self._size = 0
        self._nodeFlag = None

    #Add new child node to this tree root
    def addChild(self, value):
        if self.value == None:
            raise Exception("Add child node failed, root of subtree is None")
        child = Tree(value)
        self._children.append(child)
        self._size += 1
        child._parent = self


    #Get list of child nodes
    def getChildrenList(self):
        return self._children

    #Get one child by index
    def getChild(self, index):
        if index > self.childrenNo:
            raise Exception("Index out of range, child node number: " + str(self.childrenNo) + ", index: " + str(index))

        #mark it as visited
        self._children[index]._nodeFlag = glb.flag_dict['visited']
        return self._children[index]

    #find value in the tree, DFS
    def findDFS(self, value):
        if self.value == value:
            return self
        for subtree in self._children:
            #mark it as visited
            subtree._nodeFlag = glb.flag_dict['visited']
            result = subtree.findDFS(value)
            if result:
                return result
        return None

    #find value in the tree, BFS
    def findBFS(self, value):
        #TODO
        pass

    #remove the value
    def remove(self, value):
        #TODO, no idea now
        pass


    #To string, pre-order of the tree
    def __str__(self):
        ret = '['
        ret += str(self.value)

        for subtree in self._children:
            ret += str(subtree)

        ret += ']'
        return ret

    #reset flags
    def resetFlags(self):
        self._nodeFlag = glb.flag_dict['unchanged']
        for subtree in self._children:
            subtree.resetFlags()

    #generate a tree randomly, TODO random tree is too simple
    @classmethod
    def random(cls):
        import random
        nodeNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), nodeNo)

        tree = Tree(randomArr[0])
        for i in range(1, len(randomArr)):
            tree.addChild(randomArr[i])

        tree.resetFlags()
        return tree





