'''
Author: Fang Zhou
Date: 2015/7/16
Version: 1.0
Description: store all the necessary information of a variable. Variable objects are used by global variable stack
'''

import glb
class variable():
    def __init__(self, var_name, var_obj=None, var_flag=glb.flag_dict['new'], indexList=[], pointer=None, pointerIndexList=None):
        self.var_name = var_name
        self.var_obj = var_obj
        self.var_flag = var_flag
        self.indexList = indexList
        self.pointer = pointer
        self.pointerIndexList = pointerIndexList

    #to simplify the debug proceess
    def __str__(self):
        ret = "[name: " + str(self.var_name) + "; " \
            + "value: " + str(self.var_obj) + "; " \
            + "type: " + type(self.var_obj) + "; " \
            + "var_flag: " + str(self.var_flag) + "; " \
            + "indexList: " + str(self.indexList) + "; " \
            + "pointer: " + str(self.pointer) + "; " \
            + "pointerIndexList: " + str(self.pointerIndexList) + "]"
        return ret


