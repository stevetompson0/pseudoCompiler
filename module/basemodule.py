'''
Author: Fang Zhou
Date: 2015/8/6
Version: 1.0
Description: basic module, all other modules including loop module, branch module and function module are derived
from this module.
'''

import glb, sys

class basemodule:
    '''
    Attributions:
    end_recursive: stop running this module if True, for "return", "break" statements
    continue_flag: for "continue" statement
    '''

    __name__ = "BaseModule"

    def _func_inc(self, func_name, func_module):
        '''
        Register function
        :param func_name: function name
        :param func_module: function module
        '''

        if func_name not in glb.function_map:
            #register function in function_map for easy python function call
            # glb.function_module_map[func_name] = func_module
            glb.function_map[func_name] = \
                lambda *args, **kwargs: func_module.__call__(*args, **kwargs)
        else:
            raise NameError("function name \'{}\' already exist, conflict definition.".format(func_name))
            sys.exit(1)

    def _end_module(self):
        '''
        Tear up. Remove the variables inside this module
        '''
        from visualize.plot import resetFlagInStack
        resetFlagInStack()

        item = glb.variable_stack.pop()
        while not isinstance(item, basemodule) and len(glb.variable_stack) > 0:
            item = glb.variable_stack.pop()

    def setEnd(self):
        self.end_recursive = True

    def resetEnd(self):
        self.end_recursive = False

    def run(self):
        '''
        Overwrite this method in each derived module
        '''
        pass




