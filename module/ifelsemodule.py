'''
Author: Fang Zhou
Date: 2015/8/10
Version: 1.0
Description: if else statement module
'''

import sys, glb

from module.basemodule import basemodule

class ifelsemodule(basemodule):

    __name__ = 'IfElseModule'

    def __init__(self, conditionList, contentList,line):
        '''
        :param conditionList: list of judge conditions. E.g. if con1 else if con2 .....  [con1, con2]
        :param contentList: list of contents in each condition. E.g. if xx content1 else content2 ... [content1, content2]
        :param line: current execution line
        '''
        assert(len(conditionList) == len(contentList))
        self.conditionList = conditionList
        self.contentList = contentList
        self._judge = False
        self.end_recursive = False
        self.line = line #global current line

    def run(self):
        from visualize.plot import resetFlagInStack
        from itertools import zip_longest
        from utils.executor import evaluate
        from utils.recursive import recursive

        glb.variable_stack.append(self)
        resetFlagInStack()

        for condition, content in zip_longest(self.conditionList, self.contentList):
            # print("\tcompile if else condition: {}".format(condition))

            self._judge = evaluate(condition)

            #TODO add return value of the condition to stack

            if self._judge:
                self.line = glb.current_line + 1

                recursive(content, 0, self)
                break
            #update glb.current_line, jump to next if else condition
            else:
                glb.current_line += len(content) + 1

        self._end_module()





