'''
Author: Fang Zhou
Date: 2015/5/7
Version: 1.0
Description: Overwrite python's list class to provide customized functions
'''


import glb

class Array(list):
    __name__ = "Array"

    #initilize with an existing list or initialize an empty list
    def __init__(self, seq=[]):
        super().__init__(seq)
        # TODO Should support multi-dimension list in next version, only support 1D list currently
        self._eleFlags = [glb.flag_dict['unchanged']]*len(seq)

    @property
    def eleFlags(self):
        return self._eleFlags

    @property
    def length(self):
        return len(self)

    @property
    def isEmpty(self):
        return self.length == 0

    #change element of specific index
    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self._eleFlags[index] = glb.flag_dict['changed']

    #visit element of specific index
    def __getitem__(self, index):
        self._eleFlags[index] = glb.flag_dict['visited']
        return super().__getitem__(index)

    #append new element to the end of the list
    def append(self, p_object):
        super().append(p_object)
        self._eleFlags.append(glb.flag_dict['new'])

    #insert element at specific index
    def insert(self, index, p_object):
        super().insert(index, p_object)
        self._eleFlags.insert(index, glb.flag_dict['new'])

    #pop element at specific index or pop the last element
    def pop(self, index=None):
        if index == None:
            index = len(self)-1
        super().pop(index)
        self._eleFlags.pop(index)

    #remove the first matching element in list
    def remove(self, value):
        for index, ele in enumerate(self):
            if ele == value:
                self.pop(index)
                break

    #reverse the list
    def reverse(self):
        super().reverse()
        self._eleFlags.reverse()

    #not supported
    def sort(self):
        pass

    #swap index1 and index2
    def swap(self, index1, index2):
        if index1 >= len(self) or index2 >= len(self):
            return
        temp = self[index1]
        self[index1] = self[index2]
        self[index2] = temp
        self._eleFlags[index1] = glb.flag_dict['changed']
        self._eleFlags[index2] = glb.flag_dict['changed']

    def clear(self):
        super()
        self._eleFlags.clear()

    def resetFlags(self):
        for i in range(0, len(self._eleFlags)):
            self._eleFlags[i] = glb.flag_dict['unchanged']

    #generate a list randomly
    @classmethod
    def random(cls):
        import random
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), keyNo)

        return Array(randomArr)

