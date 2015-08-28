'''
Author: Fang Zhou
Date: 2015/5/7
Version: 1.0
Description: Overwrite python's dict class to provide customized functions
'''

import glb

class Dict(dict):
    __name__ = "Dict"

    #initilize with an existing dictionary or initialize an empty dictionary
    def __init__(self, seq={}):
        super().__init__(seq)
        self._eleFlags = {} #element flags for tracking the status of each element inside dictionary
        for key in seq.keys():
            self._eleFlags[key] = glb.flag_dict['unchanged']

    @property
    def eleFlags(self):
        return self._eleFlags

    # Add new key value pairs or change the existing key value pairs
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

        if key in self._eleFlags:
            self._eleFlags[key] = glb.flag_dict['changed']
        else:
            self._eleFlags[key] = glb.flag_dict['new']

    # get value by key
    def __getitem__(self, key):
        if key in self._eleFlags:
            self._eleFlags[key] = glb.flag_dict['visited']
        return super().__getitem__(key)


    #pop key from dictionary
    def pop(self, key):
        super().pop(key)
        self._eleFlags.pop(key)

    #update current dictionary
    def update(self, newDict):
        super().update(newDict)
        for key in newDict.keys():
            self._eleFlags[key] = glb.flag_dict['new']

    #empty the dictionary
    def clear(self):
        super().clear()
        self._eleFlags.clear()

    #reset all the element flags to unchanged
    def resetFlags(self):
        for key in self._eleFlags:
            self._eleFlags[key] = glb.flag_dict['unchanged']


    #generate a dictionary randomly
    @classmethod
    def random(cls):
        import random, string
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        keyList = random.sample(string.ascii_letters, keyNo)
        valList = random.sample(string.digits, keyNo)

        randomDict = {}
        for i in range(0, keyNo):
            randomDict[keyList[i]] = valList[i]

        return Dict(randomDict)
