'''
Author: Fang Zhou
Date: 2015/5/14
Version: 1.0
Description: Binary Min Heap, implemented by Python list
'''

import glb, heapq, math

class BinaryMinHeap():

    __name__ = "BinaryMinHeap"

    #created an empty heap or with predefined list
    def __init__(self, initList=[]):
        self._elements = list(initList)
        #heapify the elements inside list
        heapq.heapify(self._elements)

        self._eleFlags = [glb.flag_dict['unchanged']]*len(initList)

    @property
    def eleFlags(self):
        return self._eleFlags

    @property
    def elements(self):
        return self._elements

    #top element in the heap
    @property
    def top(self):
        if self.length == 0:
            return None
        return self.elements[0]

    @property
    def length(self):
        return len(self._elements)

    @property
    def isEmpty(self):
        return self.length == 0

    #define len function for heap class
    def __len__(self):
        return self.length

    #define iter function for heap, level order
    def __iter__(self):
        return iter(self.elements)

    #string format
    def __str__(self):
        return str(self.elements)

    #swap two elements
    def swap(self, index1, index2):
        temp = self.elements[index1]
        self.elements[index1] = self.elements[index2]
        self.elements[index2] = temp

        self.eleFlags[index1] = glb.flag_dict['changed']
        self.eleFlags[index2] = glb.flag_dict['changed']

    #Add a new element to the heap
    def push(self, item):
        self._elements.append(item)
        self._eleFlags.append(glb.flag_dict['new'])

        index = self.length - 1

        #sift up
        while index > 0:
            #TODO print variable status here

            parentIndex = math.floor((index-1)/2)
            if self.elements[parentIndex] > self.elements[index]:
                self.swap(parentIndex, index)
                index = parentIndex
            else:
                break

    #extract the minimal element and remove it from the heap
    def pop(self):
        if self.length == 0:
            raise Exception("Empty BinaryMinHeap, pop() terminated")

        minItem = self.elements[0]


        #reconstruct the heap tree
        index = 0
        while index < self.length:
            leftChildIndex = index*2 + 1
            rightChildIndex = index*2 + 2

            #There is no child nodes
            if leftChildIndex >= self.length:
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
                    if self._elements[leftChildIndex] <= self._elements[rightChildIndex]:
                        self.swap(index, leftChildIndex)
                        index = leftChildIndex
                    else:
                        self.swap(index, rightChildIndex)
                        index = rightChildIndex
        return minItem

    #clear the entire heap
    def clear(self):
        self._elements.clear()
        self._eleFlags.clear()

    #reset all the element flags
    def resetFlags(self):
        for i in range(0, len(self._eleFlags)):
            self._eleFlags[i] = glb.flag_dict['unchanged']

    #generate a BinaryMinHeap randomly
    @classmethod
    def random(cls):
        import random
        eleNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        #unique numbers
        randomArr = random.sample(range(100), eleNo)

        newHeap = BinaryMinHeap(randomArr)
        return newHeap
