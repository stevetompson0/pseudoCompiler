'''
Author: Fang Zhou
Date: 2015/5/20
Version: 1.0
Description: MaxPriorityQueue is similar to BinaryMaxHeap
'''

import glb, math
from structure.config import *

class MaxPriorityQueue(BinaryMaxHeap):
    """
    add_with_priority(obj, priority)
    change_priority(obj, priority)
    extract_max()
    """

    __name__ = "MaxPriorityQueue"

    def add_with_priority(self, obj, priority):
        self.push(PqueuePair(obj, priority))

    def change_priority(self, obj, priority):
        objIndex = -1
        for index, ele in enumerate(self._elements):
            if ele.obj == obj:
                objIndex = index
                break

        if objIndex != -1:
            self._eleFlags[objIndex] = glb.flag_dict['changed']
            self._elements[objIndex]._priority = priority

            #sift up first, if priority larger than parent
            parentIndex =  math.floor(objIndex/2)

            while(objIndex > 0):
                if self._elements[parentIndex] < self._elements[objIndex]:
                    self.swap(parentIndex, objIndex)
                    objIndex = parentIndex
                    parentIndex =  math.floor(objIndex/2)
                else:
                    break

            #sift down next, if priority smaller than child
            leftIndex = objIndex*2 + 1
            rightIndex = objIndex*2 + 2

            while(objIndex < len(self)):
                #no child node
                if leftIndex >= len(self):
                    break
                #left child only
                if rightIndex >= len(self):
                    if self._elements[leftIndex] > self._elements[objIndex]:
                        self.swap(leftIndex, objIndex)
                        objIndex = leftIndex
                        leftIndex = objIndex*2 + 1
                        rightIndex = objIndex*2 + 2
                    else:
                        break
                #two children
                else:
                    if self._elements[leftIndex] >= self._elements[rightIndex] and self._elements[leftIndex] > self._elements[objIndex]:
                        self.swap(leftIndex, objIndex)
                        objIndex = leftIndex
                        leftIndex = objIndex*2 + 1
                        rightIndex = objIndex*2 + 2
                    elif self._elements[leftIndex] < self._elements[rightIndex] and self._elements[rightIndex] > self._elements[objIndex]:
                        self.swap(rightIndex, objIndex)
                        objIndex = rightIndex
                        leftIndex = objIndex*2 + 1
                        rightIndex = objIndex*2 + 2
                    else:
                        break

    #extract element with maximal priority
    def extract_max(self):
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

    #generate a MaxPriorityQueue randomly
    @classmethod
    def random(cls):
        import random, string
        nodeNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        objList = random.sample(string.ascii_uppercase, nodeNo)
        priorityList = random.sample(range(50), nodeNo)

        maxQ = MaxPriorityQueue()

        #add all the elements into queue
        for i in range(0, nodeNo):
            maxQ.add_with_priority(objList[i], priorityList[i])

        #reset all eleFlags
        maxQ.resetFlags()

        return maxQ
