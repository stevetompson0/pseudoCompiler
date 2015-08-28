'''
Author: Fang Zhou
Date: 2015/8/10
Version: 1.0
Description: function module
'''

import sys, glb

from module.basemodule import basemodule

class functionmodule(basemodule):

    __name__ = 'FunctionModule'

    def __init__(self, func_name, param_list, content, line):
        self.func_name = func_name
        self.param_list = param_list
        self.content = content
        self.end_recursive = False
        self.return_list = None
        self.line = line

    # @staticmethod
    # def function_factory(obj):
    #     module = functionmodule(obj.func_name, obj.param_list, obj.content, obj.line)
    #     return module

    def __call__(self, *args, **kwargs):
        from visualize.plot import resetFlagInStack
        from utils.variable import variable
        from utils.executor import isPrimitiveType, getMatchingObject
        from utils.recursive import recursive

        #increase function call depth by one
        glb.funcall_depth += 1

        glb.variable_stack.append(self)
        resetFlagInStack()

        try:
            if len(args) + len(kwargs) != len(self.param_list):
                raise TypeError('{} positional arguments but {} given'
                                .format(len(self.param_list), len(args)+len(kwargs)))
            else:
                from itertools import zip_longest

                #combine args with values of kwargs
                args = list(args) + list(kwargs.values())

                for param, arg in zip_longest(self.param_list, args):
                    #insert parameters into global variable stack and store pointer.
                    #TODO:currently we only deal with single variable pointer. In other words, paramaters like x[1] are not handled.
                    paramVarObj = variable(param, arg)

                    #check whether variables are primitive type
                    if not isPrimitiveType(arg):
                        findObj = getMatchingObject(arg)
                        paramVarObj.pointer = findObj.var_name

                    glb.variable_stack.append([param, paramVarObj])

                #printVar()

                recursive(self.content, 0, self)

                #return function return value
                return self.return_list
        except Exception as e:
            raise Exception("Exception: \"{}\"  occurred during execution of function {}".format(e, self.func_name))
        finally:
            self._end_module()
            glb.funcall_depth -= 1
