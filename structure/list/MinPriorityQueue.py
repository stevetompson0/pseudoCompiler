'''
Author: Fang Zhou
Date: 2015/5/20
Version: 1.0
Description: MinPriorityQueue is similar to BinaryMinHeap
'''

import glb, math
from structure.config import *

class MinPriorityQueue(BinaryMinHeap):
    """
    add_with_priority(obj, priority)
    change_priority(obj, priority)
    extract_min()
    """

    __name__ = "MinPriorityQueue"

    #Add new element to the priority queue
    def add_with_priority(self, obj, priority):
        self.push(PqueuePair(obj, priority))

    #Change the priority
    def change_priority(self, obj, priority):
        #find the object index in the queue
        objIndex = -1
        for index, ele in enumerate(self._elements):
            if ele.obj == obj:
                objIndex = index
                break

        #change the priority
        if objIndex != -1:
            self._eleFlags[objIndex] = glb.flag_dict['changed']
            self._elements[objIndex]._priority = priority

            #sift up first, if priority smaller than parent
            parentIndex =  math.floor(objIndex/2)

            while objIndex > 0:
                if (self._elements[objIndex] < self._elements[parentIndex]):
                    self.swap(parentIndex, objIndex)
                    objIndex = parentIndex
                    parentIndex = math.floor(objIndex/2)
                else:
                    break

            #sift down next, if priority larger than child
            leftIndex = objIndex*2 + 1
            rightIndex = objIndex*2 + 2

            while(objIndex < len(self)):
                #no child node
                if leftIndex >= len(self):
                    break
                #left child only
                if rightIndex >= len(self):
                    if self._elements[leftIndex] < self._elements[objIndex]:
                        self.swap(leftIndex, objIndex)
                        objIndex = leftIndex
                        leftIndex = objIndex*2 + 1 #recalculate child node's index
                        rightIndex = objIndex*2 + 2
                    else:
                        break
                #two children
                else:
                    if self._elements[leftIndex] <= self._elements[rightIndex] and self._elements[leftIndex] < self._elements[objIndex]:
                        self.swap(leftIndex, objIndex)
                        objIndex = leftIndex
                        leftIndex = objIndex*2 + 1
                        rightIndex = objIndex*2 + 2
                    elif self._elements[leftIndex] > self._elements[rightIndex] and self._elements[rightIndex] < self._elements[objIndex]:
                        self.swap(rightIndex, objIndex)
                        objIndex = rightIndex
                        leftIndex = objIndex*2 + 1
                        rightIndex = objIndex*2 + 2
                    else:
                        break

    #extract element with minimal priority
    def extract_min(self):
        return self.pop().obj

    #to string
    def __str__(self):
        ret = '['
        for i in range(0, self.length):
            ret += str(self._elements[i])
            if i != self.length-1:
                ret += ","

        ret += "]"
        return ret

    #generate a MinPriorityQueue randomly
    @classmethod
    def random(cls):
        import random, string
        nodeNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        objList = random.sample(string.ascii_uppercase, nodeNo)
        priorityList = random.sample(range(50), nodeNo)

        minQ = MinPriorityQueue()

        #add all the elements into queue
        for i in range(0, nodeNo):
            minQ.add_with_priority(objList[i], priorityList[i])

        #reset flags
        minQ.resetFlags()

        return minQ


class PqueuePair:
    __name__ = "PqueueElement"

    def __init__(self, obj, priority):
        self._obj = obj
        self._priority = priority

    @property
    def obj(self):
        return self._obj

    @property
    def priority(self):
        return self._priority

    def __lt__(self, newObj):
        return self._priority < newObj._priority


    def __eq__(self, newObj):
        return self._priority == newObj._priority

    def __gt__(self, newObj):
        return self._priority > newObj._priority

    def __ge__(self, newObj):
        return self._priority >= newObj._priority

    def __le__(self, newObj):
        return self._priority <= newObj._priority

    def __str__(self):
        return "\'"+str(self.obj) + ":" + str(self.priority)+"\'"
