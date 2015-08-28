'''
Author: Fang Zhou
Date: 2015/8/10
Version: 1.0
Description: while loop module
'''


import sys, glb

from module.basemodule import basemodule
from utils.variable import variable

class whilemodule(basemodule):

    __name__ = 'WhileModule'

    def __init__(self, condition, content, line):
        self.content = content
        self.condition = condition
        self._judge = False
        self.end_recursive = False
        self.continue_flag = False
        self.line = line

    def setContinue(self):
        self.continue_flag = True

    def resetContinue(self):
        self.continue_flag = False

    def run(self):
        from visualize.plot import resetFlagInStack
        from utils.recursive import recursive
        from utils.executor import containVariableInGlbStack, getVariableFromGlbStack, evaluate

        glb.variable_stack.append(self)
        resetFlagInStack()

        #judge the condition
        self._judge = evaluate(self.condition)

        #TODO: we may also print out the condition result

        #navigates to the next line -- start of the content
        self.line = glb.current_line + 1

        while self._judge:

            recursive(self.content, 0, self)

            #clear flags after one loop
            resetFlagInStack()

            #re-evaluate the judge condition
            self._judge = evaluate(self.condition)

            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()

        self._end_module()
