'''
Author: Fang Zhou
Date: 2015/8/6
Version: 1.0
Description: for loop module
'''

import sys, glb

from module.basemodule import basemodule
from utils.variable import variable

class formodule(basemodule):

    __name__ = 'ForModule'

    def __init__(self, param, content, line):
        self.content = content
        self.iter_var = param[0]
        self.loop_range = param[1]
        self.range_var_name  = param[2] #if we use for xx = x to xx step xx, this will be "", if we use for x in VAR, this will be VAR
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
        from utils.executor import containVariableInGlbStack, getVariableFromGlbStack

        glb.variable_stack.append(self)
        resetFlagInStack()

        #insert iterate variable inside global variable stack
        iterVarObj = variable(self.iter_var, None)
        glb.variable_stack.append([self.iter_var, iterVarObj])
        setPointer = False #whether we should treat iter_var as a pointer

        var_being_iter = getVariableFromGlbStack(self.range_var_name)

        if self.range_var_name and containVariableInGlbStack(self.range_var_name):# for x in range_var_name
            setPointer = True

        #navigates to the next line -- start of the content
        self.line = glb.current_line + 1

        #start the loop
        for index, value in enumerate(self.loop_range):
            #check end_recursive flag
            if self.end_recursive:
                break

            iterVarObj.var_obj = value
            iterVarObj.var_flag = glb.flag_dict['changed']

            if setPointer:
                iterVarObj.pointerIndexList = [index]
                iterVarObj.pointer = getVariableFromGlbStack(self.range_var_name).var_name

            if var_being_iter:
                #update index of this variable
                var_being_iter.indexList = [index]

            # printVar() #do not need to specially call printVar for iter_var
            recursive(self.content, 0, self)

            #clear flags after one loop
            resetFlagInStack()

            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()

        self._end_module()
