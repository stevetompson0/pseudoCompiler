'''
Author: Fang Zhou
Date: 2015/8/6
Version: 1.0
Description: global module, which all global variables are stored. The first module invoked by pseudo program.
'''

import sys, glb

from module.basemodule import basemodule

class glbmodule(basemodule):

    __name__ = 'GlobalModule'

    def __init__(self, content, line):
        self.content = content #list of lines
        self.line = line
        self.end_recursive = False

    def run(self):
        import utils.recursive as recursive
        from visualize.plot import resetFlagInStack

        glb.variable_stack.append(self)
        resetFlagInStack()

        recursive.recursive(self.content, 0, self)

        self._end_module()
