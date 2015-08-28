'''
Author: Fang Zhou
Date: 2015/5/7
Version: 1.0
Description: Stack data structure
'''

from structure.config import *

class Stack(Array):
    '''
    top
    1) push(item)
    2) pop()
    '''

    __name__ = "Stack"

    @property
    def top(self):
        if self:
            return self[len(self)-1]

    def push(self, item):
        self.append(item)

    def pop(self):
        if len(self) == 0:
            raise Exception("Empty Stack")
        super().pop()