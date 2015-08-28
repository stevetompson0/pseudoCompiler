'''
Author: Fang Zhou
Date: 2015/5/20
Version: 1.0
Description: A disjoint-set data structure, also called a union–find data structure or merge–find set,
is a data structure that keeps track of a set of elements partitioned into a number of disjoint (nonoverlapping) subsets.

It supports two useful operations:
i) Find: Determine which subset a particular element is in.
Find typically returns an item from this set that serves as its "representative".
Also, by comparing the result of two Find operations, one can determine whether two elements are in the same subset.

ii)Union: Join two subsets into a single subset.
'''

import glb

class DisjointSet(dict):
    __name__ = "DisjointSet"

    #init an empty set
    def __init__(self):
        self._eleFlags = {}

    @property
    def eleFlags(self):
        return self._eleFlags

    #create a new independent set
    def add(self, item):
        self[item] = item
        self._eleFlags[item] = glb.flag_dict['new']

    #find which subset a particular element is in
    def find(self, item):
        parent = self[item]

        #trace back to the top parent
        while self[parent] != parent:
            parent = self[parent]

        #TODO may add balance here, such as self[item] = parent
        self[item] = parent
        return parent

    #join two subsets into a single subset.
    def union(self, element1, element2):
        set1 = self.find(element1)
        set2 = self.find(element2)

        if set1 != set2:
            #mark each element in set2 as changed
            for key in self:
                if self.find(key) == set2:
                    self._eleFlags[key] = glb.flag_dict['changed']

            #change root of set2 to set1
            self[set2] = set1

    #reset all the element flags to unchanged
    def resetFlags(self):
        for key in self._eleFlags:
            self._eleFlags[key] = glb.flag_dict['unchanged']

    #generate a disjointset randomly
    @classmethod
    def random(cls):
        import random, string
        eleNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        eleList = random.sample(string.ascii_uppercase, eleNo)

        dset = DisjointSet()
        #add all the elements into set
        for ele in eleList:
            dset.add(ele)

        #union
        for i in range(0, eleNo):
            if i%2 == 0:
                dset.union(eleList[0], eleList[i])
            else:
                dset.union(eleList[1], eleList[i]) #if i%2 == 1, eleList must has index 1

        return dset