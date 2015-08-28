'''
Author: Fang Zhou
Date: 2015/5/9
Version: 1.0
Description: Doubly LinkedList data structure
'''

import glb

class ListNode():
    '''
    Node of linked list
    '''
    def __init__(self, item, prev=None, next=None):
        self._item = item
        self._prev = prev
        self._next = next

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, nprev):
        self._prev = nprev

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, nnext):
        self._next = nnext

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, nitem):
        self._item = nitem

    def __str__(self):
        return str(self._item)


class LinkedList(list):

    __name__ = "LinkedList"

    #initilize an empty LinkedList
    def __init__(self):
        self._eleFlags = []

    @property
    def eleFlags(self):
        return self._eleFlags

    @property
    def length(self):
        return len(self)

    @property
    def isEmpty(self):
        return self.length == 0

    @property
    def head(self):
        if self:
            return self[0]
        else:
            return None

    #returns the element at the specified position in this list, Type: ListNode
    def get(self, index):
        if index >= self.length:
            raise Exception("LinkedList index out of range, index: " + str(index))

        #TODO mark it as changed temporarily
        self._eleFlags[index] = glb.flag_dict['changed']

        return self[index]

    #add new element to end of the list
    def addLast(self, item):
        newNode = ListNode(item)

        #set links between nodes
        if self.length > 0:
            newNode.prev = self[self.length-1]
            self[self.length-1].next = newNode

        self.append(newNode)
        self._eleFlags.append(glb.flag_dict['new'])

    #insert element the specified position in this list
    def add(self, index, item):
        if index > self.length:
            return
        else:
            newNode = ListNode(item)
            if index < self.length:
                rightNode = self.get(index)
                newNode.next = rightNode
                rightNode.prev = newNode

            if index-1 >= 0:
                leftNode = self.get(index-1)
                leftNode.next = newNode
                newNode.prev = leftNode

            self.insert(index, newNode)
            self._eleFlags.insert(index, glb.flag_dict['new'])


    #search the linkedlist based on values, return index number
    def search(self, obj):
        for index in range(0, self.length):
            if self[index].item == obj:
                return index
        return -1 #not found

    #pop the last node from the LinkedList
    def pop(self):
        if self.length == 0:
            raise Exception("Empty LinkedList, pop operation terminated.")

        if self.length > 1:
            self[self.length-2].next = None
            self._eleFlags[self.length-2] = glb.flag_dict['changed']

        self._eleFlags.pop()
        return super().pop(self.length-1)

    #removes and returns the element at the specified position, by default the index is 0
    def remove(self, index=0):
        if index >= self.length:
            raise Exception("Index out of range, remove operation terminated.")

        leftNode = None
        rightNode = None

        if index-1 >= 0:
            leftNode = self[index-1]
        if index+1 < self.length:
            rightNode = self[index+1]

        if leftNode:
            leftNode.next = rightNode
            self._eleFlags[index-1] = glb.flag_dict['changed']
        if rightNode:
            rightNode.prev = leftNode
            self._eleFlags[index+1] = glb.flag_dict['changed']

        self._eleFlags.pop(index)
        return super().pop(index)

    #remove the first occurrence of the specified element from this list, if it is present
    def removeValue(self, obj):
        index = self.search(obj)
        if index == -1:
            return None
        return self.remove(index)

    #swap two nodes
    def swap(self, index1, index2):
        if index1 >= self.length or index2 >= self.length:
            return

        tempObj = self[index1].item
        self[index1].item = self[index2].item
        self[index2].item = tempObj
        self._eleFlags[index1] = glb.flag_dict['changed']
        self._eleFlags[index2] = glb.flag_dict['changed']


    #clear whole LinkedList
    def clear(self):
        super().clear()
        self._eleFlags.clear()

    #reset all element flags
    def resetFlags(self):
        for i in range(0, len(self._eleFlags)):
            self._eleFlags[i] = glb.flag_dict['unchanged']

    #to string
    def __str__(self):
        listStr = "["
        for i in range(0, self.length):
            listStr += str(self[i])
            if i != self.length - 1:
                listStr += ", "
        listStr += "]"
        return listStr


    #generates a LinkedList randomly
    @classmethod
    def random(cls):
        import random
        keyNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        randomArr = random.sample(range(100), keyNo)
        newlist = LinkedList()

        for num in randomArr:
            newlist.addLast(num)
        return newlist
