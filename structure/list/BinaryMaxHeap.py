'''
Author: Fang Zhou
Date: 2015/5/15
Version: 1.0
Description: Binary Max Heap, inherit from BinaryMinHeap
'''

import glb, heapq, math
from structure.config import *

class BinaryMaxHeap(BinaryMinHeap):

    __name__ = "BinaryMaxHeap"

    #created an empty heap or with predefined list
    def __init__(self, initList=[]):

        #define eleFlags before push
        self._eleFlags = []
        self._elements = []

        #heapify the elements inside list
        for ele in initList:
            self.push(ele)

        #reset all flags to unchanged
        self.resetFlags()



    #Add a new element to the heap
    def push(self, item):
        self._elements.append(item)
        self._eleFlags.append(glb.flag_dict['new'])

        index = self.length - 1

        #sift up
        while index > 0:
            #TODO print variable status here

            parentIndex = math.floor((index-1)/2)
            if self.elements[parentIndex] < self.elements[index]:
                self.swap(parentIndex, index)
                index = parentIndex
            else:
                break

    #extract the maximal element and remove it from the heap
    def pop(self):
        if self.length == 0:
            raise Exception("Empty BinaryMaxHeap, pop() terminated")

        maxItem = self.elements[0]

        #reconstruct the heap tree
        index = 0
        while index < self.length:
            leftChildIndex = index*2 + 1
            rightChildIndex = index*2 + 2

            #There is no child nodes
            if leftChildIndex >= self.length:
                #The top element will finally pop out from here, no need to do the comparison between child node and parent node
                self._elements.pop(index)
                self._eleFlags.pop(index)
                break
            else:
                #TODO print variable status here

                #Only has left node
                if rightChildIndex >= self.length:
                    self.swap(index, leftChildIndex)
                    index = leftChildIndex
                #Two nodes
                else:
                    if self._elements[leftChildIndex] >= self._elements[rightChildIndex]:
                        self.swap(index, leftChildIndex)
                        index = leftChildIndex
                    else:
                        self.swap(index, rightChildIndex)
                        index = rightChildIndex
        return maxItem

    #generate a BinaryMaxHeap randomly
    @classmethod
    def random(cls):
        import random
        eleNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        #unique numbers
        randomArr = random.sample(range(100), eleNo)

        newHeap = BinaryMaxHeap(randomArr)
        return newHeap
