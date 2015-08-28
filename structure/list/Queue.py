'''
Author: Fang Zhou
Date: 2015/5/9
Version: 1.0
Description: Queue data structure
'''

from structure.config import *

class Queue(Array):
    __name__ = "Queue"

    def enqueue(self, item):
        self.append(item)

    def dequeue(self):
        if len(self) == 0:
            raise Exception("Empty Queue")
        return self.pop(0)
